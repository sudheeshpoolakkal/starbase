const fs = require('node:fs');

function mysqlOptions(env = process.env) {
  const host = env.DB_HOST || '127.0.0.1';
  const tidbCloud = /(^|\.)tidbcloud\.com$/i.test(host);
  if (tidbCloud && env.DB_SSL === 'false') {
    throw new Error('TiDB Cloud requires TLS. Set DB_SSL=true.');
  }
  const ssl = env.DB_SSL === 'true' || tidbCloud
    ? {
      rejectUnauthorized: true,
      verifyIdentity: true,
      minVersion: 'TLSv1.2',
      ...(env.DB_SSL_CA ? { ca: fs.readFileSync(env.DB_SSL_CA) } : {}),
    } : undefined;
  return {
    host,
    port: Number(env.DB_PORT || 3306),
    user: env.DB_USER || 'materia',
    password: env.DB_PASSWORD || '',
    database: env.DB_NAME || 'material_optimization_db',
    charset: 'utf8mb4',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 100,
    connectTimeout: 10000,
    ssl,
  };
}

module.exports = { mysqlOptions };
