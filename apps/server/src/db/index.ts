import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';
import * as schema from './schema.js';

let db: ReturnType<typeof drizzle> | null = null;

export async function initDb() {
  if (db) return db;

  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
  });

  db = drizzle(pool, { schema });

  // Test connection
  const result = await pool.query('SELECT NOW()');
  console.log('Database connected:', result.rows[0]);

  return db;
}

export function getDb() {
  if (!db) throw new Error('Database not initialized');
  return db;
}
