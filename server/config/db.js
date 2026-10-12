// MySQL is mandatory at runtime. SQLite is confined to disposable unit tests.
if (process.env.NODE_ENV === "test" && process.env.USE_SQLITE === "true") {
  module.exports = require("../tests/fixtures/sqlite-db");
} else {
  const mysql = require("mysql2/promise");
  const { mysqlOptions } = require('./mysql-options');
  const pool = mysql.createPool(mysqlOptions());
  const ready = pool.getConnection().then((connection) => {
    connection.release();
    console.log("Connected to MySQL.");
  }).catch(async (error) => {
    await pool.end();
    throw new Error(`MySQL is unavailable (${error.code || "connection error"}). Configure DB_HOST, DB_PORT, DB_USER, DB_PASSWORD and DB_NAME. No fallback catalog is used.`);
  });
  module.exports = {
    ready,
    driver: () => "mysql",
    execute: async (sql, params = []) => { await ready; return pool.execute(sql, params); },
    query: async (sql, params = []) => { await ready; return pool.query(sql, params); },
    getConnection: async () => { await ready; return pool.getConnection(); },
    close: async () => { await ready; await pool.end(); },
  };
}
