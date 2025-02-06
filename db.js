const { Pool } = require('pg');

const pool = new Pool({
  user: 'your-db-username',
  host: 'localhost',
  database: 'TaskTickTornado',
  password: 'your-db-password',
  port: 5432,
});

module.exports = pool;