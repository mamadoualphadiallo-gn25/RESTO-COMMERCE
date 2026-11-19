from pathlib import Path
import sqlite3
from contextlib import contextmanager

ROOT = Path(__file__).resolve().parents[1]
DB_DIR = ROOT / "database"
DB_PATH = DB_DIR / "gesco_restaurant.sqlite"

def connect():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=15000")
    return conn

@contextmanager
def transaction():
    db = connect()
    try:
        db.execute("BEGIN IMMEDIATE")
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def initialize():
    with transaction() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS products (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          sku TEXT UNIQUE, name TEXT NOT NULL,
          category TEXT NOT NULL DEFAULT 'Général',
          unit TEXT NOT NULL DEFAULT 'unité',
          purchase_price INTEGER NOT NULL DEFAULT 0 CHECK(purchase_price>=0),
          sale_price INTEGER NOT NULL CHECK(sale_price>=0),
          stock REAL NOT NULL DEFAULT 0 CHECK(stock>=0),
          active INTEGER NOT NULL DEFAULT 1,
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS sales (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          sale_number TEXT NOT NULL UNIQUE,
          channel TEXT NOT NULL CHECK(channel IN ('restaurant','commerce')),
          subtotal INTEGER NOT NULL, discount INTEGER NOT NULL DEFAULT 0,
          total INTEGER NOT NULL, payment_method TEXT NOT NULL DEFAULT 'espèces',
          status TEXT NOT NULL DEFAULT 'paid',
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS sale_items (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
          product_id INTEGER NOT NULL REFERENCES products(id),
          product_name TEXT NOT NULL, quantity REAL NOT NULL CHECK(quantity>0),
          unit_price INTEGER NOT NULL, line_total INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS stock_movements (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          product_id INTEGER NOT NULL REFERENCES products(id),
          movement_type TEXT NOT NULL CHECK(movement_type IN ('in','out','sale','adjustment')),
          quantity REAL NOT NULL, note TEXT,
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_sales_created ON sales(created_at);
        CREATE INDEX IF NOT EXISTS idx_items_sale ON sale_items(sale_id);
        """)
