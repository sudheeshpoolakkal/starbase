// Transfer complete normalized snapshots independently of the running local import.
// Checkpoints describe committed file positions, never inferred database row counts.
const fs = require('node:fs');
const fsp = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const readline = require('node:readline');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../..');

async function* snapshotRows(filename, onChunk = () => {}) {
  if (filename.endsWith('.jsonl')) {
    const stream = fs.createReadStream(filename);
    stream.on('data', onChunk);
    const lines = readline.createInterface({ input: stream, crlfDelay: Infinity });
    let header;
    try {
      for await (const line of lines) {
        if (!line.trim()) continue;
        const value = JSON.parse(line);
        if (!header) {
          header = value;
          if (!header.source || !Number.isSafeInteger(header.records)) throw new Error('Invalid JSONL header.');
          yield { source: header.source, records: header.records };
        } else yield { material: value };
      }
      if (!header) throw new Error('Empty snapshot.');
    } finally { lines.close(); stream.destroy(); }
  } else {
    const bytes = await fsp.readFile(filename);
    onChunk(bytes);
    const bundle = JSON.parse(bytes);
    if (!bundle.source || !Array.isArray(bundle.materials)) throw new Error('Invalid JSON bundle.');
    yield { source: bundle.source, records: bundle.materials.length };
    for (const material of bundle.materials) yield { material };
  }
}

async function inspectSnapshot(entry, projectRoot = root) {
  const filename = path.resolve(projectRoot, entry.normalizedFile);
  const hash = crypto.createHash('sha256');
  const coverage = {}, samples = [];
  const samplePositions = new Set([0, Math.floor(entry.expectedRecords / 2), entry.expectedRecords - 1]);
  let source, records = 0;
  for await (const item of snapshotRows(filename, chunk => hash.update(chunk))) {
    if (item.source) {
      source = item.source;
      assert.equal(source.key, entry.sourceKey, 'Snapshot source differs from inventory.');
      assert.equal(source.checksum, entry.originalSourceChecksum, 'Source checksum differs from inventory.');
      assert.equal(item.records, entry.expectedRecords, 'Declared snapshot count differs from inventory.');
      continue;
    }
    const material = item.material;
    if (!material || typeof material.externalId !== 'string' || !material.externalId) throw new Error('Invalid snapshot record identity.');
    if (samplePositions.has(records)) samples.push(material);
    for (const [key, value] of Object.entries(material.properties || {})) {
      if (value !== null) coverage[key] = (coverage[key] || 0) + 1;
    }
    records++;
  }
  assert.equal(records, entry.expectedRecords, 'Actual snapshot count differs from inventory.');
  assert.equal(hash.digest('hex'), entry.normalizedSha256, 'Normalized snapshot SHA-256 differs from inventory.');
  return { ...entry, filename, source, coverage, samples, verifiedRecords: records };
}

async function* batches(snapshot, batchSize, offset = 0) {
  if (!Number.isSafeInteger(offset) || offset < 0 || offset > snapshot.expectedRecords) throw new Error('Invalid saved checkpoint offset.');
  let processed = 0, materials = [];
  for await (const item of snapshotRows(snapshot.filename)) {
    if (item.source) continue;
    processed++;
    if (processed <= offset) continue;
    materials.push(item.material);
    if (materials.length === batchSize) {
      yield { materials, processed };
      materials = [];
    }
  }
  if (materials.length) yield { materials, processed };
  assert.equal(processed, snapshot.expectedRecords, 'Snapshot changed after verification.');
}

async function transferBatches(snapshot, batchSize, checkpoint, operations) {
  // A crash between import and checkpoint intentionally replays the last batch.
  // The catalog's stable source/external-ID upserts make that replay idempotent.
  const offset = checkpoint?.normalized_checksum === snapshot.normalizedSha256
    ? Number(checkpoint.processed_records) : 0;
  for await (const batch of batches(snapshot, batchSize, offset)) {
    await operations.importBatch({ source: snapshot.source, materials: batch.materials });
    await operations.saveCheckpoint(batch.processed);
    operations.progress?.(batch.processed);
  }
}

async function inspectTarget(db) {
  const [[version]] = await db.query('SELECT TIDB_VERSION() AS version');
  const [tls] = await db.query("SHOW SESSION STATUS LIKE 'Ssl_cipher'");
  if (!tls[0]?.Value) throw new Error('The cloud connection is not encrypted.');
  const [columns] = await db.execute('SELECT TABLE_NAME,COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=DATABASE()');
  const existing = new Map();
  for (const column of columns) {
    const table = column.TABLE_NAME.toLowerCase();
    if (!existing.has(table)) existing.set(table, new Set());
    existing.get(table).add(column.COLUMN_NAME.toLowerCase());
  }
  for (const [table, fields] of Object.entries({
    material: ['material_id', 'name', 'category_id', 'source_id'],
    material_category: ['category_id', 'name'], data_source: ['source_id', 'name', 'note'],
    property: ['property_id', 'property_key', 'name', 'unit'],
    material_property: ['material_id', 'property_id', 'numeric_value', 'text_value'],
    manufacturing_process: ['process_id', 'name'], material_process: ['material_id', 'process_id'],
    users: ['user_id', 'email', 'password_hash'], projects: ['project_id', 'owner_id', 'name'],
  })) {
    if (existing.has(table) && fields.some(field => !existing.get(table).has(field))) {
      throw new Error(`Existing ${table} has an incompatible schema. Use a separate empty Starbase database; do not run the teammate SQL in it.`);
    }
  }
  return { engine: 'TiDB', version: version.version, encrypted: true, existingTables: existing.size };
}

async function reconcileSource(db, snapshot, refreshSummary) {
  const [sources] = await db.execute('SELECT name,note,url,license,data_kind,version,checksum FROM Data_Source WHERE source_key=?', [snapshot.sourceKey]);
  assert.equal(sources.length, 1, 'Source provenance row missing.');
  assert.deepEqual(sources[0], {
    name: snapshot.source.name, note: snapshot.source.note || '', url: snapshot.source.url,
    license: snapshot.source.license, data_kind: snapshot.source.kind,
    version: snapshot.source.version || '', checksum: snapshot.source.checksum,
  }, 'Source provenance differs from the snapshot.');
  const summary = await refreshSummary(snapshot.sourceKey);
  assert.equal(summary.count, snapshot.expectedRecords, `${snapshot.sourceKey}: database record count mismatch.`);
  const actualCoverage = Object.fromEntries(summary.coverage.map(item => [item.propertyKey, Number(item.count)]));
  assert.deepEqual(actualCoverage, snapshot.coverage, `${snapshot.sourceKey}: property coverage mismatch.`);
  for (const sample of snapshot.samples) {
    const [records] = await db.execute('SELECT m.material_id,m.name,m.description,m.source_url,m.metadata_json,m.search_terms FROM Material m JOIN Data_Source s USING(source_id) WHERE s.source_key=? AND m.external_id=?', [snapshot.sourceKey, sample.externalId]);
    assert.equal(records.length, 1, 'Sample accession missing or duplicated.');
    const record = records[0];
    assert.equal(record.name, sample.name);
    assert.equal(record.description || '', sample.description || '');
    assert.equal(record.source_url, sample.sourceUrl);
    assert.equal(record.search_terms || '', (sample.metadata?.searchAliases || []).join(' '));
    assert.deepEqual(JSON.parse(record.metadata_json || '{}'), sample.metadata || {});
    const [values] = await db.execute('SELECT p.property_key,mp.numeric_value,mp.text_value FROM Material_Property mp JOIN Property p USING(property_id) WHERE mp.material_id=?', [record.material_id]);
    const actual = Object.fromEntries(values.map(value => [value.property_key, value.numeric_value === null ? value.text_value : Number(value.numeric_value)]));
    const expected = Object.fromEntries(Object.entries(sample.properties || {}).filter(([, value]) => value !== null));
    assert.deepEqual(Object.keys(actual).sort(), Object.keys(expected).sort());
    for (const [key, value] of Object.entries(expected)) {
      if (typeof value === 'number') assert.ok(Math.abs(actual[key] - value) <= Math.max(1, Math.abs(value)) * 1e-10, `Sample ${key} differs.`);
      else assert.equal(actual[key], value);
    }
  }
  return summary;
}

async function importSnapshot(db, snapshot, batchSize, importBundle, refreshSummary) {
  const [saved] = await db.execute('SELECT * FROM Catalog_Import_Progress WHERE source_key=?', [snapshot.sourceKey]);
  const checkpoint = saved[0];
  if (checkpoint?.normalized_checksum === snapshot.normalizedSha256 && checkpoint.status === 'complete') {
    await reconcileSource(db, snapshot, refreshSummary);
    await db.execute("UPDATE Data_Source SET import_state='complete' WHERE source_key=?", [snapshot.sourceKey]);
    console.log(`${snapshot.sourceKey}: previously complete; counts, coverage and samples verified`);
    return;
  }
  await db.execute("UPDATE Data_Source SET import_state='importing',summary_json=NULL WHERE source_key=?", [snapshot.sourceKey]);
  const offset = checkpoint?.normalized_checksum === snapshot.normalizedSha256 ? Number(checkpoint.processed_records) : 0;
  await db.execute("INSERT INTO Catalog_Import_Progress (source_key,normalized_checksum,expected_records,processed_records,status) VALUES (?,?,?,?,'importing') ON DUPLICATE KEY UPDATE normalized_checksum=VALUES(normalized_checksum),expected_records=VALUES(expected_records),processed_records=VALUES(processed_records),status='importing'", [snapshot.sourceKey, snapshot.normalizedSha256, snapshot.expectedRecords, offset]);
  console.log(`${snapshot.sourceKey}: starting at committed file position ${offset.toLocaleString()}/${snapshot.expectedRecords.toLocaleString()}`);
  let lastLog = Date.now();
  await transferBatches(snapshot, batchSize, checkpoint, {
    importBatch: bundle => importBundle(bundle, { refreshSummary: false }),
    saveCheckpoint: processed => db.execute('UPDATE Catalog_Import_Progress SET processed_records=? WHERE source_key=? AND normalized_checksum=?', [processed, snapshot.sourceKey, snapshot.normalizedSha256]),
    progress: processed => {
      if (Date.now() - lastLog > 15000 || processed === snapshot.expectedRecords) {
        console.log(`${snapshot.sourceKey}: ${processed.toLocaleString()}/${snapshot.expectedRecords.toLocaleString()} committed`);
        lastLog = Date.now();
      }
    },
  });
  await reconcileSource(db, snapshot, refreshSummary);
  await db.execute("UPDATE Data_Source SET import_state='complete' WHERE source_key=?", [snapshot.sourceKey]);
  await db.execute("UPDATE Catalog_Import_Progress SET status='complete' WHERE source_key=?", [snapshot.sourceKey]);
  console.log(`${snapshot.sourceKey}: complete; counts, coverage and samples verified`);
}

async function stageContribution(db, filename) {
  const contribution = JSON.parse(await fsp.readFile(filename, 'utf8'));
  if (!/^[a-f0-9]{64}$/.test(contribution.originalSqlSha256) || !Array.isArray(contribution.materials) || !contribution.materials.length) throw new Error('Invalid contribution review file.');
  await db.execute(`CREATE TABLE IF NOT EXISTS Contribution_Review (
    contribution_checksum VARCHAR(64) NOT NULL, external_id VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL, review_status VARCHAR(40) NOT NULL,
    payload_json MEDIUMTEXT NOT NULL, submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(contribution_checksum,external_id))`);
  const connection = await db.getConnection();
  try {
    await connection.beginTransaction();
    for (const material of contribution.materials) {
      await connection.execute("INSERT INTO Contribution_Review (contribution_checksum,external_id,name,review_status,payload_json) VALUES (?,?,?,'needs-citations',?) ON DUPLICATE KEY UPDATE name=VALUES(name),payload_json=VALUES(payload_json)", [contribution.originalSqlSha256, String(material.material_id), material.material_name, JSON.stringify(material)]);
    }
    await connection.commit();
  } catch (error) { await connection.rollback(); throw error; }
  finally { connection.release(); }
  const [[count]] = await db.execute('SELECT COUNT(*) AS total FROM Contribution_Review WHERE contribution_checksum=?', [contribution.originalSqlSha256]);
  assert.equal(Number(count.total), contribution.materials.length);
  console.log(`${count.total} teammate materials preserved in Contribution_Review; awaiting citations`);
}

function parseArgs(args) {
  const options = { mode: 'verify', batchSize: 1000, inventory: path.join(root, 'docs/cloud-data-inventory.json'), env: path.join(root, 'server/.env.tidb') };
  let modes = 0;
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (['--verify', '--check', '--import'].includes(arg)) { options.mode = arg.slice(2); modes++; }
    else if (['--env', '--inventory', '--source', '--batch-size', '--stage-teammate'].includes(arg)) {
      if (!args[i + 1] || args[i + 1].startsWith('--')) throw new Error(`Missing value for ${arg}.`);
      const value = args[++i];
      if (arg === '--source') options.sources = value.split(',');
      else if (arg === '--batch-size') options.batchSize = Number(value);
      else if (arg === '--stage-teammate') options.contribution = path.resolve(value);
      else options[arg.slice(2)] = path.resolve(value);
    } else throw new Error(`Unknown option ${arg}.`);
  }
  if (modes > 1 || !Number.isSafeInteger(options.batchSize) || options.batchSize < 1 || options.batchSize > 5000) throw new Error('Choose one mode and a batch size from 1 to 5000.');
  if (options.contribution && options.mode !== 'import') throw new Error('--stage-teammate requires --import.');
  return options;
}

function loadCloudEnv(filename) {
  const values = require('dotenv').parse(fs.readFileSync(filename));
  for (const key of ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']) {
    if (!values[key] || /^(your-|replace_with)/.test(values[key])) throw new Error(`Configure ${key} in the private TiDB environment file.`);
  }
  if (values.DB_SSL !== 'true') throw new Error('The TiDB environment file must set DB_SSL=true.');
  for (const key of Object.keys(process.env)) if (key.startsWith('DB_')) delete process.env[key];
  Object.assign(process.env, values, { USE_SQLITE: 'false' });
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const inventory = JSON.parse(await fsp.readFile(options.inventory, 'utf8'));
  const entries = inventory.sources.filter(entry => !options.sources || options.sources.includes(entry.sourceKey));
  if (!entries.length || options.sources?.some(key => !entries.some(entry => entry.sourceKey === key))) throw new Error('Unknown source selection.');
  const snapshots = [];
  for (const entry of entries) {
    const snapshot = await inspectSnapshot(entry);
    snapshots.push(snapshot);
    console.log(`${entry.sourceKey}: verified SHA-256, ${snapshot.verifiedRecords.toLocaleString()} parsed records, property coverage`);
  }
  console.log(`${snapshots.length} collections; ${snapshots.reduce((sum, entry) => sum + entry.verifiedRecords, 0).toLocaleString()} verified source records`);
  if (options.mode === 'verify') return;
  loadCloudEnv(options.env);
  const db = require('../config/db');
  try {
    await db.ready;
    const target = await inspectTarget(db);
    console.log(JSON.stringify(target));
    if (options.mode === 'check') return;
    const { ready } = require('../services/catalog');
    await ready;
    const { importBundle } = require('./import-catalog');
    const { refreshSourceSummary } = require('../services/catalogSummary');
    await db.execute(`CREATE TABLE IF NOT EXISTS Catalog_Import_Progress (
      source_key VARCHAR(100) PRIMARY KEY, normalized_checksum VARCHAR(64) NOT NULL,
      expected_records BIGINT NOT NULL, processed_records BIGINT NOT NULL DEFAULT 0,
      status VARCHAR(20) NOT NULL, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)`);
    for (const snapshot of snapshots) await importSnapshot(db, snapshot, options.batchSize, importBundle, refreshSourceSummary);
    if (options.contribution) await stageContribution(db, options.contribution);
    console.log('Selected catalog sources transferred and reconciled. Application cutover and original-archive upload remain separate steps.');
  } finally { await db.close(); }
}

if (require.main === module) main().catch(error => { console.error(error.message); process.exitCode = 1; });
module.exports = { snapshotRows, inspectSnapshot, batches, transferBatches, inspectTarget, reconcileSource, importSnapshot, stageContribution, parseArgs };
