import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            crop TEXT NOT NULL,
            disease_code TEXT NOT NULL,
            disease_name TEXT NOT NULL,
            confidence REAL NOT NULL,
            severity TEXT NOT NULL,
            symptoms TEXT,
            organic_treatment TEXT,
            chemical_treatment TEXT,
            status TEXT NOT NULL DEFAULT 'Pending',
            green_pct REAL,
            yellow_pct REAL,
            brown_pct REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_scan(crop, disease_code, disease_name, confidence, severity, symptoms, organic, chemical, green_pct, yellow_pct, brown_pct):
    """Saves a leaf diagnostic scan to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Serialize symptoms list to JSON string
    symptoms_str = json.dumps(symptoms) if isinstance(symptoms, list) else symptoms
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO scans (
            timestamp, crop, disease_code, disease_name, confidence, severity, 
            symptoms, organic_treatment, chemical_treatment, status, 
            green_pct, yellow_pct, brown_pct
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        timestamp, crop, disease_code, disease_name, confidence, severity,
        symptoms_str, organic, chemical, 'Pending', green_pct, yellow_pct, brown_pct
    ))
    
    scan_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return scan_id

def get_scan_history(limit=50):
    """Retrieves list of scans from database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scans ORDER BY id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    
    history = []
    for row in rows:
        scan = dict(row)
        # Deserialize symptoms
        try:
            scan['symptoms'] = json.loads(scan['symptoms'])
        except Exception:
            pass
        history.append(scan)
        
    conn.close()
    return history

def update_scan_status(scan_id, new_status):
    """Updates the agricultural treatment action state for a leaf scan."""
    if new_status not in ['Pending', 'Treated', 'Monitoring']:
        return False
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE scans SET status = ? WHERE id = ?', (new_status, scan_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

# Self-initialize when run directly
if __name__ == '__main__':
    print("Initializing AgriVision SQLite Database...")
    init_db()
    print("Database ready at:", DB_PATH)
