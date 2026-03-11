const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const dbPath = path.resolve(process.cwd(), 'brain_cloud.db');

// Remove existing database if it exists
if (fs.existsSync(dbPath)) {
  fs.unlinkSync(dbPath);
  console.log('🗑️  Existing database removed');
}

// Create new database
const db = new Database(dbPath);

// Create lore table
db.exec(`
  CREATE TABLE IF NOT EXISTS lore (
    id TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    resonance REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );
`);

console.log('✨ Database initialized successfully');
console.log(`📍 Location: ${dbPath}`);

// Create index for better query performance
db.prepare('CREATE INDEX IF NOT EXISTS idx_url ON lore(url)').run();

console.log('🔍 Indexes created');

db.close();
console.log('✅ brain_cloud.db ready for operation');
