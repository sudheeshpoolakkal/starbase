const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const { mysqlOptions } = require('../config/mysql-options');
const { inspectSnapshot, transferBatches, inspectTarget, reconcileSource, parseArgs } = require('../scripts/transfer-tidb');

async function fixture(t) {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'starbase-transfer-'));
  t.after(() => fs.rm(directory, { recursive: true, force: true }));
  const source = { key: 'transfer-test', checksum: 'a'.repeat(64) };
  const materials = Array.from({ length: 5 }, (_, i) => ({ externalId: `row-${i}`, name: `Material ${i}`, properties: { density: i + 1, tensileStrength: i % 2 ? null : i } }));
  const bytes = [JSON.stringify({ source, records: 5 }), ...materials.map(m => JSON.stringify(m))].join('\n') + '\n';
  await fs.writeFile(path.join(directory, 'test.jsonl'), bytes);
  const entry = { sourceKey: source.key, normalizedFile: 'test.jsonl', expectedRecords: 5, normalizedSha256: crypto.createHash('sha256').update(bytes).digest('hex'), originalSourceChecksum: source.checksum };
  return { directory, entry, materials, bytes };
}

test('TiDB validates the certificate and hostname; TLS cannot be disabled', () => {
  const options = mysqlOptions({ DB_HOST: 'example.tidbcloud.com', DB_PORT: '4000' });
  assert.equal(options.ssl.rejectUnauthorized, true);
  assert.equal(options.ssl.verifyIdentity, true);
  assert.equal(options.ssl.minVersion, 'TLSv1.2');
  assert.throws(() => mysqlOptions({ DB_HOST: 'example.tidbcloud.com', DB_SSL: 'false' }), /requires TLS/);
  assert.equal(mysqlOptions({ DB_HOST: '127.0.0.1' }).ssl, undefined);
  assert.equal(mysqlOptions({ DB_HOST: 'another-cloud.example', DB_SSL: 'true' }).ssl.rejectUnauthorized, true);
});

test('preflight parses the entire stream, preserves zero, and rejects corruption or truncation', async t => {
  const { directory, entry, bytes } = await fixture(t);
  const snapshot = await inspectSnapshot(entry, directory);
  assert.equal(snapshot.verifiedRecords, 5);
  assert.deepEqual(snapshot.coverage, { density: 5, tensileStrength: 3 });
  assert.deepEqual(snapshot.samples.map(m => m.externalId), ['row-0', 'row-2', 'row-4']);
  await fs.writeFile(path.join(directory, 'test.jsonl'), bytes.replace('Material 1', 'Material X'));
  await assert.rejects(inspectSnapshot(entry, directory), /SHA-256/);
  await fs.writeFile(path.join(directory, 'test.jsonl'), bytes.split('\n').slice(0, -2).join('\n'));
  await assert.rejects(inspectSnapshot(entry, directory), /Actual snapshot count/);
});

test('crash after a committed import replays that batch; arbitrary database row counts never skip file rows', async t => {
  const { directory, entry } = await fixture(t);
  const snapshot = await inspectSnapshot(entry, directory);
  const database = new Map();
  let checkpoint, calls = 0;
  const importBatch = async bundle => {
    calls++;
    for (const material of bundle.materials) database.set(material.externalId, material);
  };
  await assert.rejects(transferBatches(snapshot, 2, null, {
    importBatch,
    saveCheckpoint: async processed => {
      if (processed === 4) throw new Error('simulated disconnection after commit');
      checkpoint = { normalized_checksum: entry.normalizedSha256, processed_records: processed };
    },
  }), /simulated disconnection/);
  assert.equal(database.size, 4);
  assert.equal(checkpoint.processed_records, 2);
  await transferBatches(snapshot, 2, checkpoint, {
    importBatch,
    saveCheckpoint: async processed => { checkpoint.processed_records = processed; },
  });
  assert.deepEqual([...database.keys()], ['row-0', 'row-1', 'row-2', 'row-3', 'row-4']);
  assert.equal(calls, 4); // Includes a safe replay of rows 2 and 3.
  assert.equal(checkpoint.processed_records, 5);
});

test('a different snapshot digest restarts from the beginning; invalid offsets stop', async t => {
  const { directory, entry } = await fixture(t);
  const snapshot = await inspectSnapshot(entry, directory);
  const loaded = [];
  await transferBatches(snapshot, 2, { normalized_checksum: 'b'.repeat(64), processed_records: 5 }, {
    importBatch: async bundle => loaded.push(...bundle.materials.map(m => m.externalId)), saveCheckpoint: async () => {},
  });
  assert.equal(loaded.length, 5);
  await assert.rejects(transferBatches(snapshot, 2, { normalized_checksum: entry.normalizedSha256, processed_records: 6 }, { importBatch: async () => {}, saveCheckpoint: async () => {} }), /Invalid saved checkpoint/);
});

test('read-only target inspection rejects the teammate schema before catalog initialization', async () => {
  const db = {
    query: async sql => sql.startsWith('SELECT') ? [[{ version: 'TiDB test' }]] : [[{ Value: 'TLS_AES_256_GCM_SHA384' }]],
    execute: async () => [[{ TABLE_NAME: 'material', COLUMN_NAME: 'material_id' }, { TABLE_NAME: 'material', COLUMN_NAME: 'material_name' }]],
  };
  await assert.rejects(inspectTarget(db), /incompatible schema/);
  db.execute = async () => [[]];
  assert.equal((await inspectTarget(db)).encrypted, true);
  db.query = async sql => sql.startsWith('SELECT') ? [[{ version: 'TiDB test' }]] : [[]];
  await assert.rejects(inspectTarget(db), /not encrypted/);
});

test('CLI rejects ambiguous modes, unknown options, and oversized batches', () => {
  assert.equal(parseArgs([]).mode, 'verify');
  assert.throws(() => parseArgs(['--verify', '--import']));
  assert.throws(() => parseArgs(['--batch-size', '25000']));
  assert.throws(() => parseArgs(['--env']));
  assert.throws(() => parseArgs(['--unknown']));
});

test('reconciliation executes sample joins with overlapping source/material column names', async () => {
  const { DatabaseSync } = require('node:sqlite');
  const connection = new DatabaseSync(':memory:');
  try {
    connection.exec(`
      CREATE TABLE Data_Source(source_id INTEGER PRIMARY KEY,source_key TEXT,name TEXT,note TEXT,url TEXT,license TEXT,data_kind TEXT,version TEXT,checksum TEXT);
      CREATE TABLE Material(material_id INTEGER PRIMARY KEY,source_id INTEGER,external_id TEXT,name TEXT,description TEXT,source_url TEXT,metadata_json TEXT,search_terms TEXT);
      CREATE TABLE Property(property_id INTEGER PRIMARY KEY,property_key TEXT);
      CREATE TABLE Material_Property(material_id INTEGER,property_id INTEGER,numeric_value REAL,text_value TEXT);
    `);
    const source = { key: 'sample-source', name: 'Source name', note: '', url: 'https://example.org/source', license: 'CC BY 4.0', kind: 'experimental', version: '1', checksum: 'a'.repeat(64) };
    const material = { externalId: 'sample-1', name: 'Material name', description: 'Sample', sourceUrl: 'https://example.org/sample', metadata: { propertyConditions: { density: '23 C' } }, properties: { density: 0 } };
    connection.prepare('INSERT INTO Data_Source VALUES (1,?,?,?,?,?,?,?,?)').run(source.key,source.name,source.note,source.url,source.license,source.kind,source.version,source.checksum);
    connection.prepare('INSERT INTO Material VALUES (1,1,?,?,?,?,?,?)').run(material.externalId,material.name,material.description,material.sourceUrl,JSON.stringify(material.metadata),'');
    connection.exec("INSERT INTO Property VALUES (1,'density'); INSERT INTO Material_Property VALUES (1,1,0,NULL);");
    const db = { execute: async (sql, params) => [connection.prepare(sql).all(...params).map(row => ({ ...row }))] };
    const snapshot = { sourceKey: source.key, source, expectedRecords: 1, coverage: { density: 1 }, samples: [material] };
    const refresh = async () => ({ count: 1, coverage: [{ propertyKey: 'density', count: 1 }] });
    await reconcileSource(db, snapshot, refresh);
    connection.exec('UPDATE Material_Property SET numeric_value=7');
    await assert.rejects(reconcileSource(db, snapshot, refresh), /Sample density differs/);
  } finally { connection.close(); }
});
