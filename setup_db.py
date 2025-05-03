import sqlite3

DB_PATH = "earthquakes.db"

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create earthquakes table with time_utc and time_utc_human
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS earthquakes (
        id TEXT PRIMARY KEY,
        time_utc INTEGER,
        mag REAL,
        place TEXT,
        longitude REAL,
        latitude REAL,
        depth_km REAL,
        time_utc_human TEXT
    );
    """)

    # Create avg_mag table (average magnitude of earthquakes)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avg_mag (
        id INTEGER PRIMARY KEY,
        average_mag REAL
    );
    """)

    # Create total_earthquakes table (total count of earthquakes)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS total_earthquakes (
        id INTEGER PRIMARY KEY,
        total_count INTEGER
    );
    """)

    # Create latest_earthquake table (latest earthquake data)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS latest_earthquake (
        id TEXT PRIMARY KEY,
        time_utc INTEGER,
        mag REAL,
        place TEXT,
        longitude REAL,
        latitude REAL,
        depth_km REAL,
        time_utc_human TEXT
    );
    """)

    # Create max_mag table (maximum magnitude earthquake)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS max_mag (
        id TEXT PRIMARY KEY,
        max_mag REAL,
        place TEXT,
        time_utc INTEGER,
        time_utc_human TEXT
    );
    """)

    conn.commit()
    print("✅ Database and tables setup completed.")
    conn.close()

if __name__ == "__main__":
    setup_database()
