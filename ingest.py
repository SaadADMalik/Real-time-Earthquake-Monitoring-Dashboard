import sqlite3
import pandas as pd
from datetime import datetime, timedelta, timezone
import time

DB_PATH = "earthquakes.db"
BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query.csv"

def fetch_earthquakes_last_hour():
    # Get the current UTC time
    end_time = datetime.utcnow()
    # Calculate the time for one hour ago
    start_time = end_time - timedelta(hours=1)

    # Convert start and end times to string format for the API
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Construct the API URL to fetch earthquakes that occurred in the last hour
    params = {
        "format": "csv",
        "starttime": start_time_str,
        "endtime": end_time_str,
        "orderby": "time",  # Most recent first
    }
    url = BASE_URL + "?" + "&".join(f"{k}={v}" for k, v in params.items())
    print(f"Fetching earthquake data from: {url}")
    
    # Fetch the data
    df = pd.read_csv(url, parse_dates=["time"])

    # If data is fetched, return it, otherwise return an empty dataframe
    if not df.empty:
        return df
    else:
        return pd.DataFrame()  # Return an empty dataframe if no data is fetched

def insert_earthquakes(df):
    if df.empty:
        print("✅ No new data to ingest.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure the correct columns from the latest earthquake data
    df["time_utc"] = df["time"].astype("int64") // 1_000_000  # Convert time to UTC in milliseconds
    df["time_utc_human"] = df["time"].dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Insert data into the earthquakes table using batch operation
    data = [(row['id'], row['time_utc'], row['mag'], row['place'], row['longitude'], row['latitude'], row['depth'], row['time_utc_human']) for index, row in df.iterrows()]
    cursor.executemany("""
        INSERT OR REPLACE INTO earthquakes (id, time_utc, mag, place, longitude, latitude, depth_km, time_utc_human)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    # Update aggregate tables
    cursor.execute("""
    INSERT OR REPLACE INTO total_earthquakes (id, total_count)
    VALUES (1, (SELECT COUNT(*) FROM earthquakes));
    """)

    cursor.execute("""
    INSERT OR REPLACE INTO avg_mag (id, average_mag)
    VALUES (1, (SELECT AVG(mag) FROM earthquakes));
    """)

    # Delete any existing rows in the latest_earthquake table before inserting the new data
    cursor.execute("DELETE FROM latest_earthquake;")  # Delete all rows in latest_earthquake

    # Insert the latest earthquake data (most recent one)
    cursor.execute("""
    INSERT OR REPLACE INTO latest_earthquake (id, time_utc, mag, place, longitude, latitude, depth_km, time_utc_human)
    SELECT id, time_utc, mag, place, longitude, latitude, depth_km, time_utc_human
    FROM earthquakes
    ORDER BY time_utc DESC
    LIMIT 1;
    """)

    # Insert max magnitude data
    cursor.execute("""
    INSERT OR REPLACE INTO max_mag (id, max_mag, place, time_utc, time_utc_human)
    SELECT id, MAX(mag), place, time_utc, time_utc_human
    FROM earthquakes;
    """)

    conn.commit()
    print(f"✅ Ingested {len(df)} new earthquake(s) and updated aggregates.")
    conn.close()


if __name__ == "__main__":
    while True:
        # Step 1: Fetch the earthquakes data for the last hour
        print("⏳ Fetching earthquake data from the last hour...")
        df = fetch_earthquakes_last_hour()
        insert_earthquakes(df)  # Insert the new earthquake data into the database
        
        # Wait for 1 hour before the next fetch
        print("🕐 Waiting 1 hour to fetch the next batch of earthquake data...")
        time.sleep(3600)  # Wait for 1 hour before the next fetch
