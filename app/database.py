import sqlite3

DB_FILE = "url.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            access_count INTEGER NOT NULL DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()