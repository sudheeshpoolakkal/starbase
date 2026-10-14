const { test } = require('node:test');
const assert = require('node:assert/strict');
const { encodeRecord, decodeRecord, descriptionSql } = require('../services/recordStorage');

function material(file, mask) {
  const basis = [['formationEnergy', 'computed'], ['bandGap', 'computed'], ['density', 'derived from DFT unit cell']];
  return {
    externalId: 'alexandria-109',
    description: 'Alexandria PBE relaxed crystal. Computed properties; original structure is retained in the source archive.',
    sourceUrl: 'https://alexandria.icams.rub.de/',
    metadata: { formula: 'Al2O3', accession: 'alexandria-109', sourceFile: file, spaceGroup: null, energyAboveHullEvPerAtom: 0, unitCellVolumeAngstrom3: 99.5, propertyBasis: Object.fromEntries(basis.filter((_, index) => mask & (1 << index))) },
  };
}
function row(value, key, encoded) {
  return { source_key: key, external_id: value.externalId, description: encoded.description, source_url: encoded.sourceUrl, metadata_json: JSON.stringify(encoded.metadata) };
}

test('Alexandria storage preserves all fields, missing properties, zero and null across both snapshot types', () => {
  for (const key of ['alexandria-pbe', 'alexandria-pbe-hull']) {
    for (const file of ['alexandria_00000.json.bz2', 'alexandria_00057.json.bz2', 'convex_hull.json.bz2']) {
      for (let mask = 0; mask < 8; mask++) {
        const value = material(file, mask);
        const before = structuredClone(value);
        const encoded = encodeRecord(value, key);
        assert.equal(encoded.description, null);
        assert.equal(encoded.sourceUrl, null);
        assert.deepEqual(decodeRecord(row(value, key, encoded)), { description: value.description, sourceUrl: value.sourceUrl, metadata: value.metadata });
        assert.deepEqual(value, before);
      }
    }
  }
});

test('SQL keyword screening restores the packed description and keeps custom descriptions', () => {
  const { DatabaseSync } = require('node:sqlite');
  const database = new DatabaseSync(':memory:');
  try {
    database.exec('CREATE TABLE Material(description TEXT,metadata_json TEXT); CREATE TABLE Data_Source(source_key TEXT);');
    const value = material('alexandria_00001.json.bz2', 7);
    const encoded = encodeRecord(value, 'alexandria-pbe');
    database.prepare('INSERT INTO Material VALUES (?,?)').run(encoded.description, JSON.stringify(encoded.metadata));
    database.exec("INSERT INTO Data_Source VALUES ('alexandria-pbe')");
    const search = database.prepare(`SELECT COUNT(*) AS count FROM Material m CROSS JOIN Data_Source s WHERE ${descriptionSql()} LIKE ?`);
    assert.equal(search.get('%relaxed crystal%').count, 1);
    database.exec("UPDATE Material SET description='Custom conditions'");
    assert.equal(search.get('%relaxed crystal%').count, 0);
    assert.equal(search.get('%Custom conditions%').count, 1);
    database.exec("UPDATE Material SET description=NULL; UPDATE Data_Source SET source_key='unrelated'");
    assert.equal(search.get('%relaxed crystal%').count, 0);
  } finally { database.close(); }
});

test('unknown metadata, property evidence and sources remain unpacked; custom descriptions and citations survive', () => {
  const key = 'alexandria-pbe';
  for (const change of [value => { value.metadata.extra = 1; }, value => { value.metadata.accession = 'different'; }, value => { value.metadata.propertyBasis.density = 'experimental'; }, value => { value.metadata.sourceFile = 'new-format.json'; }]) {
    const value = material('alexandria_00001.json.bz2', 7);
    change(value);
    assert.deepEqual(encodeRecord(value, key), { description: value.description, sourceUrl: value.sourceUrl, metadata: value.metadata });
  }
  const value = material('alexandria_00001.json.bz2', 7);
  assert.deepEqual(encodeRecord(value, 'unrelated-source'), { description: value.description, sourceUrl: value.sourceUrl, metadata: value.metadata });
  value.description = 'Record-specific conditions';
  value.sourceUrl = 'https://example.org/record/109';
  assert.deepEqual(decodeRecord(row(value, key, encodeRecord(value, key))), { description: value.description, sourceUrl: value.sourceUrl, metadata: value.metadata });
});
