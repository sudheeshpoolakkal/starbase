// Rank in SQL before fetching record metadata, so large research catalogs stay bounded.
const db = require('../config/db');
const { descriptionSql } = require('./recordStorage');
const { ready, getCatalog, getSummary, definitions, costRank, resistanceRank } = require('./catalog');
const { recommend, validateRequirements, numericRules } = require('./recommendation');
const factors = { strength: 'tensileStrength', lightness: 'density', cost: 'cost', thermal: 'thermalConductivity', stiffness: 'bulkModulus', vacuum: 'collectedVolatileCondensableMaterial' };
const ids = Object.fromEntries(definitions.map(([key], i) => [key, i + 1]));
const invert = new Set(['lightness', 'cost', 'vacuum']);
const cost = alias => `CASE ${alias}.text_value WHEN 'Low' THEN 1 WHEN 'Moderate' THEN 2 WHEN 'Medium' THEN 2 WHEN 'High' THEN 3 WHEN 'Very High' THEN 4 ELSE NULL END`;
const resistance = alias => `CASE ${alias}.text_value WHEN 'Poor' THEN 1 WHEN 'Fair' THEN 2 WHEN 'Moderate' THEN 2 WHEN 'Good' THEN 3 WHEN 'Excellent' THEN 4 ELSE NULL END`;
const base = 'FROM Material m JOIN Material_Category c ON c.category_id=m.category_id JOIN Data_Source s ON s.source_id=m.source_id';

async function recommendCatalog(input) {
  const requirements = validateRequirements(input);
  await ready;
  const bounds = {};
  // Read numeric index edges instead of grouping every property row and loading
  // millions of clustered Material pages just to find min/max values.
  for(const [factor,property] of Object.entries(factors)) {
    if(property==='cost') {
      const [[row]]=await db.execute(`SELECT MIN(${cost('mp')}) AS lo,MAX(${cost('mp')}) AS hi FROM Material_Property mp JOIN Material m ON m.material_id=mp.material_id JOIN Data_Source s ON s.source_id=m.source_id WHERE mp.property_id=? AND s.source_key IS NOT NULL AND COALESCE(s.import_state,'complete')='complete'`,[ids[property]]);
      bounds[factor]=row.lo==null?[0,0]:[Number(row.lo),Number(row.hi)];
    } else {
      const edge=async direction=>{
        const force=db.driver()==='mysql'?'FORCE INDEX (material_numeric_index)':'';
        const [[row]]=await db.execute(`SELECT mp.numeric_value AS value FROM Material_Property mp ${force} JOIN Material m ON m.material_id=mp.material_id JOIN Data_Source s ON s.source_id=m.source_id WHERE mp.property_id=? AND mp.numeric_value IS NOT NULL AND s.source_key IS NOT NULL AND COALESCE(s.import_state,'complete')='complete' ORDER BY mp.numeric_value ${direction} LIMIT 1`,[ids[property]]);
        return row?Number(row.value):0;
      };
      bounds[factor]=[await edge('ASC'),await edge('DESC')];
    }
  }
  const aliases = new Map();
  const joins = [];
  const expression = property => {
    if (!aliases.has(property)) {
      const alias = `v${aliases.size}`;
      aliases.set(property, alias);
      joins.push(`LEFT JOIN Material_Property ${alias} ON ${alias}.material_id=m.material_id AND ${alias}.property_id=${ids[property]}`);
    }
    return property === 'cost' ? cost(aliases.get(property)) : `${aliases.get(property)}.numeric_value`;
  };
  const where = [], params = [], active = [], scores = [];
  const weightTotal = Object.values(requirements.weights).reduce((a,b) => a+b,0);
  for (const [factor, property] of Object.entries(factors)) {
    const weight = requirements.weights[factor];
    if (!weight) continue;
    const value = expression(property), [lo, hi] = bounds[factor];
    active.push(`${value} IS NOT NULL`);
    const normalized = hi === lo ? '1' : invert.has(factor) ? `((${hi}-${value})*1.0/${hi-lo})` : `((${value}-${lo})*1.0/${hi-lo})`;
    scores.push(`CASE WHEN ${value} IS NULL THEN 0 ELSE ${normalized}*${weight/weightTotal*100} END`);
  }
  where.push(`(${active.join(' OR ')})`);
  for (const [key,[property, operation]] of Object.entries(numericRules)) {
    if (requirements[key] === undefined || ['volume','maxWeight'].includes(key)) continue;
    const value = expression(property);
    where.push(`(${value} IS NOT NULL AND ${value}${operation==='min'?'>=':'<='}?)`);
    params.push(requirements[key]);
  }
  if (requirements.maxWeight) {
    const value = expression('density');
    where.push(`(${value} IS NOT NULL AND ${value}<=?)`);
    params.push(requirements.maxWeight*1000/requirements.volume);
  }
  for (const [key,column] of [['category','c.name'],['dataKind','s.data_kind']]) {
    if (requirements[key]) { where.push(`${column}=?`); params.push(requirements[key]); }
  }
  if (requirements.keyword) {
    const term = `%${requirements.keyword.replace(/[!%_]/g,'!$&')}%`;
    where.push(`(LOWER(m.name) LIKE LOWER(?) ESCAPE '!' OR LOWER(${descriptionSql()}) LIKE LOWER(?) ESCAPE '!' OR LOWER(c.name) LIKE LOWER(?) ESCAPE '!' OR LOWER(COALESCE(m.search_terms,'')) LIKE LOWER(?) ESCAPE '!' OR EXISTS (SELECT 1 FROM Material_Application ma JOIN Application a ON a.application_id=ma.application_id WHERE ma.material_id=m.material_id AND LOWER(a.name) LIKE LOWER(?) ESCAPE '!'))`);
    params.push(term,term,term,term,term);
  }
  for (const [key,table,column] of [['application','Application','application_id'],['process','Manufacturing_Process','process_id']]) {
    if (!requirements[key]) continue;
    const association = key==='application'?'Material_Application':'Material_Process';
    where.push(`EXISTS (SELECT 1 FROM ${association} ma JOIN ${table} a ON a.${column}=ma.${column} WHERE ma.material_id=m.material_id AND a.name=?)`);
    params.push(requirements[key]);
  }
  if (requirements.maxCost) { const value=expression('cost'); where.push(`(${value} IS NOT NULL AND ${value}<=?)`); params.push(costRank[requirements.maxCost]); }
  if (requirements.corrosionResistance) {
    expression('corrosionResistance'); const value=resistance(aliases.get('corrosionResistance'));
    where.push(`(${value} IS NOT NULL AND ${value}>=?)`); params.push(resistanceRank[requirements.corrosionResistance]);
  }
  const summary = await getSummary();
  const coverage = property => summary.coverage.find(p => p.propertyKey === property)?.count || 0;
  // A required property is an intersection, not a union of every ranking priority.
  // Start with the smallest supported property index; density alone spans millions
  // of records, while tensile/thermal/vacuum requirements usually span thousands.
  const required = Object.entries(numericRules)
    .filter(([key]) => requirements[key] !== undefined && !['volume', 'maxWeight'].includes(key))
    .map(([, [property]]) => property);
  if (requirements.maxWeight) required.push('density');
  if (requirements.maxCost) required.push('cost');
  if (requirements.corrosionResistance) required.push('corrosionResistance');
  const activeProperties = Object.entries(factors).filter(([factor]) => requirements.weights[factor] > 0).map(([, property]) => property);
  if (!required.length && activeProperties.length === 1) required.push(activeProperties[0]);
  const driverProperty = required.sort((a, b) => coverage(a) - coverage(b))[0];
  const sourceCount = summary.sources.filter(s => !requirements.dataKind || s.dataKind === requirements.dataKind)
    .reduce((sum, s) => sum + s.count, 0);
  const straight = db.driver() === 'mysql' ? 'STRAIGHT_JOIN' : 'JOIN';
  let ranked = base;
  if (driverProperty && coverage(driverProperty) <= sourceCount) {
    const index = db.driver() === 'mysql' ? 'FORCE INDEX (material_numeric_index)' : '';
    ranked = `FROM Material_Property required_value ${index}
      ${straight} Material m ON m.material_id=required_value.material_id
      ${straight} Material_Category c ON c.category_id=m.category_id
      ${straight} Data_Source s ON s.source_id=m.source_id`;
    where.push(`required_value.property_id=${ids[driverProperty]}`);
  } else if (requirements.category && (!requirements.dataKind ||
      (summary.categories.find(c => c.name === requirements.category)?.count || 0) < sourceCount)) {
    ranked = `FROM Material_Category c ${straight} Material m ON m.category_id=c.category_id
      ${straight} Data_Source s ON s.source_id=m.source_id`;
  } else if (requirements.dataKind) {
    const index = db.driver() === 'mysql' ? 'FORCE INDEX (material_external_unique)' : '';
    ranked = `FROM Data_Source s ${straight} Material m ${index} ON m.source_id=s.source_id
      ${straight} Material_Category c ON c.category_id=m.category_id`;
  }
  ranked += ` ${joins.join(' ')}`;
  const predicate = where.join(' AND ');
  const scope = "s.source_key IS NOT NULL AND COALESCE(s.import_state,'complete')='complete'";
  let count, top;
  const denseProperty = activeProperties.find(property => property !== 'cost' && coverage(property) > 1000 && coverage(property) > summary.total / 2);
  const unconstrained = Object.keys(requirements).every(key => key === 'weights');
  const denseBounds = denseProperty && bounds[Object.keys(factors).find(f => factors[f] === denseProperty)];
  if (unconstrained && denseProperty && denseBounds[0] !== denseBounds[1] &&
      activeProperties.filter(p => p !== denseProperty).every(p => coverage(p) < 100000)) {
    // Partition unrestricted rankings into sparse-property records and records
    // whose only active measurement is dense (currently density). The latter
    // have a monotonic score, so the numeric index gives a safe score threshold.
    // This preserves exact counts and ranking without sorting millions of rows.
    const sparse = activeProperties.filter(p => p !== denseProperty);
    const score = `ROUND(${scores.join('+')},1)`;
    const denseFactor = Object.keys(factors).find(f => factors[f] === denseProperty);
    const denseValue = expression(denseProperty);
    const denseWeight = requirements.weights[denseFactor] / weightTotal * 100;
    const [lo, hi] = bounds[denseFactor];
    const index = db.driver() === 'mysql' ? 'FORCE INDEX (material_numeric_index)' : '';
    const denseBase = `FROM Material_Property required_value ${index}
      ${straight} Material m ON m.material_id=required_value.material_id
      ${straight} Material_Category c ON c.category_id=m.category_id
      ${straight} Data_Source s ON s.source_id=m.source_id ${joins.join(' ')}`;
    const denseWhere = `${scope} AND required_value.property_id=${ids[denseProperty]}
      AND required_value.numeric_value IS NOT NULL ${sparse.map(p => `AND ${expression(p)} IS NULL`).join(' ')}`;
    let sparseTop = [], sparseCount = 0, overlap = 0;
    if (sparse.length) {
      const sparseBase = `FROM (SELECT DISTINCT material_id FROM Material_Property ${index}
        WHERE property_id IN (${sparse.map(p => ids[p]).join(',')}) AND (numeric_value IS NOT NULL OR text_value IS NOT NULL)) eligible
        ${straight} Material m ON m.material_id=eligible.material_id
        ${straight} Material_Category c ON c.category_id=m.category_id
        ${straight} Data_Source s ON s.source_id=m.source_id ${joins.join(' ')}`;
      const sparseWhere = `${scope} AND (${sparse.map(p => `${expression(p)} IS NOT NULL`).join(' OR ')})`;
      const [[row]] = await db.execute(`SELECT COUNT(*) AS total,COALESCE(SUM(${denseValue} IS NOT NULL),0) AS overlap ${sparseBase} WHERE ${sparseWhere}`);
      sparseCount = Number(row.total); overlap = Number(row.overlap);
      [sparseTop] = await db.execute(`SELECT m.material_id,${score} AS score ${sparseBase} WHERE ${sparseWhere} ORDER BY score DESC,m.material_id LIMIT 50`);
    }
    const direction = invert.has(denseFactor) ? 'ASC' : 'DESC';
    const [seed] = await db.execute(`SELECT m.material_id,${score} AS score ${denseBase} WHERE ${denseWhere} ORDER BY required_value.numeric_value ${direction} LIMIT 50`);
    const finalists = [...sparseTop, ...seed].sort((a,b) => b.score-a.score || a.material_id-b.material_id).slice(0,50);
    let denseTop = seed;
    if (seed.length && hi !== lo) {
      const threshold = Number(finalists.at(-1).score);
      // Include the entire rounded-score tie bucket, then break ties by ID.
      const fraction = (threshold - 0.0500001) / denseWeight;
      const cutoff = invert.has(denseFactor) ? hi - fraction*(hi-lo) : lo + fraction*(hi-lo);
      [denseTop] = await db.execute(`SELECT m.material_id,${score} AS score ${denseBase} WHERE ${denseWhere}
        AND required_value.numeric_value ${invert.has(denseFactor) ? '<=' : '>='} ? ORDER BY score DESC,m.material_id LIMIT 50`,[cutoff]);
    }
    top = [...sparseTop, ...denseTop].sort((a,b) => b.score-a.score || a.material_id-b.material_id).slice(0,50);
    count = sparseCount + coverage(denseProperty) - overlap;
  } else {
    const [[row]] = await db.execute(`SELECT COUNT(*) AS total ${ranked} WHERE ${scope} AND ${predicate}`,params);
    count = Number(row.total);
    [top] = await db.execute(`SELECT m.material_id,ROUND(${scores.join('+')},1) AS score ${ranked} WHERE ${scope} AND ${predicate} ORDER BY score DESC,m.material_id LIMIT 50`,params);
  }
  // Explanations are a bounded sample, not a second full inverse catalog scan.
  // Evaluate them with the same JS rules so SQL NULL logic cannot hide missing data.
  const sampleBase = db.driver() === 'mysql'
    ? `FROM Material m FORCE INDEX (PRIMARY) STRAIGHT_JOIN Material_Category c ON c.category_id=m.category_id STRAIGHT_JOIN Data_Source s ON s.source_id=m.source_id`
    : base;
  const [sample] = await db.execute(`SELECT m.material_id ${sampleBase} WHERE ${scope} ORDER BY m.material_id LIMIT 100`);
  const result = recommend(await getCatalog(top.map(r=>r.material_id)),requirements,{bounds});
  const excluded = recommend(await getCatalog(sample.map(r=>r.material_id)),requirements,{bounds}).excluded;
  return {...result, total:summary.total,count,shown:top.length,excluded,excludedCount:summary.total-count};
}
module.exports = { recommendCatalog };
