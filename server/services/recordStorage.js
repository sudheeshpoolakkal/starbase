// Alexandria's source-wide constants and repeated JSON keys dominate its row
// size. This reversible codec changes storage only; API records retain their
// original description, URL and complete metadata.
const sources = new Set(['alexandria-pbe', 'alexandria-pbe-hull']);
const description = 'Alexandria PBE relaxed crystal. Computed properties; original structure is retained in the source archive.';
const sourceUrl = 'https://alexandria.icams.rub.de/';
const metadataKeys = ['formula', 'accession', 'sourceFile', 'spaceGroup', 'energyAboveHullEvPerAtom', 'unitCellVolumeAngstrom3', 'propertyBasis'];
const basis = [['formationEnergy', 'computed'], ['bandGap', 'computed'], ['density', 'derived from DFT unit cell']];

function encodeRecord(material, sourceKey) {
  const original = { description: material.description || '', sourceUrl: material.sourceUrl, metadata: material.metadata || {} };
  const m = original.metadata;
  if (!sources.has(sourceKey) || Object.keys(m).length !== metadataKeys.length || metadataKeys.some(key => !Object.hasOwn(m, key)) || m.accession !== material.externalId || typeof m.formula !== 'string') return original;
  const file = m.sourceFile === 'convex_hull.json.bz2' ? -1 : /^alexandria_\d{5}\.json\.bz2$/.test(m.sourceFile || '') ? Number(m.sourceFile.slice(11, 16)) : null;
  if (file === null || !m.propertyBasis || typeof m.propertyBasis !== 'object' || Array.isArray(m.propertyBasis)) return original;
  if (Object.entries(m.propertyBasis).some(([key, value]) => !basis.some(([expectedKey, expectedValue]) => key === expectedKey && value === expectedValue))) return original;
  const mask = basis.reduce((value, [key], index) => value | (Object.hasOwn(m.propertyBasis, key) ? 1 << index : 0), 0);
  return {
    description: original.description === description ? null : original.description,
    sourceUrl: original.sourceUrl === sourceUrl ? null : original.sourceUrl,
    metadata: { _alexandria: [1, m.formula, file, m.spaceGroup, m.energyAboveHullEvPerAtom, m.unitCellVolumeAngstrom3, mask] },
  };
}

function decodeRecord(row) {
  const metadata = row.metadata_json ? JSON.parse(row.metadata_json) : {};
  const packed = metadata._alexandria;
  if (!sources.has(row.source_key) || Object.keys(metadata).length !== 1 || !Array.isArray(packed) || packed.length !== 7 || packed[0] !== 1) {
    return { description: row.description, sourceUrl: row.source_url, metadata };
  }
  const [, formula, file, spaceGroup, energyAboveHullEvPerAtom, unitCellVolumeAngstrom3, mask] = packed;
  if (!Number.isInteger(file) || file < -1 || file > 99999 || !Number.isInteger(mask) || mask < 0 || mask > 7) throw new Error('Invalid Alexandria storage metadata.');
  return {
    description: row.description === null ? description : row.description,
    sourceUrl: row.source_url === null ? sourceUrl : row.source_url,
    metadata: {
      formula, accession: row.external_id,
      sourceFile: file === -1 ? 'convex_hull.json.bz2' : `alexandria_${String(file).padStart(5, '0')}.json.bz2`,
      spaceGroup, energyAboveHullEvPerAtom, unitCellVolumeAngstrom3,
      propertyBasis: Object.fromEntries(basis.filter((_, index) => mask & (1 << index))),
    },
  };
}

// SQL screening must search the same description that API hydration returns.
function descriptionSql(materialAlias = 'm', sourceAlias = 's') {
  const literal = description.replaceAll("'", "''");
  const prefix = '{"_alexandria":[1,';
  return `COALESCE(${materialAlias}.description, CASE WHEN ${sourceAlias}.source_key IN ('alexandria-pbe','alexandria-pbe-hull') AND SUBSTR(${materialAlias}.metadata_json,1,${prefix.length})='${prefix}' THEN '${literal}' ELSE '' END)`;
}

module.exports = { encodeRecord, decodeRecord, descriptionSql };
