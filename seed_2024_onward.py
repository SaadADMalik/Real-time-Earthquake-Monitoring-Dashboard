from datetime import datetime, timezone
import sqlite3
import pandas as pd
from datetime import timedelta

DB_PATH = "earthquakes.db"
BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query.csv"

def seed_historical_data():
    conn = sqlite3.connect(DB_PATH)
    current = datetime(2024, 1, 1, tzinfo=timezone.utc)  # Make start date timezone-aware
    end = datetime.now(timezone.utc)  # Make end date timezone-aware

    while current < end:
        next_chunk = current + timedelta(days=30)
        if next_chunk > end:
            next_chunk = end

        params = {
            "format": "csv",
            "starttime": current.strftime("%Y-%m-%d"),
            "endtime": next_chunk.strftime("%Y-%m-%d"),
            "orderby": "time-asc"
        }
        url = BASE_URL + "?" + "&".join(f"{k}={v}" for k, v in params.items())

        df = pd.read_csv(url, parse_dates=["time"])
        if not df.empty:
            df["time_utc"] = (df["time"].astype("int64") // 1_000_000)
            df["time_utc_human"] = df["time"].dt.strftime('%Y-%m-%dT%H:%M:%SZ')

            subset = df[["id", "time_utc", "mag", "place", "longitude", "latitude", "depth", "time_utc_human"]]
            subset.columns = ["id", "time_utc", "mag", "place", "longitude", "latitude", "depth_km", "time_utc_human"]

            # Insert the data into the earthquakes table
            subset.to_sql("earthquakes", conn, if_exists="append", index=False, method="multi", chunksize=100)
            print(f"✅ Imported {len(subset)} rows: {current.date()} → {next_chunk.date()}")

            # Update aggregate tables
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO total_earthquakes (id, total_count)
            VALUES (1, (SELECT COUNT(*) FROM earthquakes));
            """)
            cursor.execute("""
            INSERT OR REPLACE INTO avg_mag (id, average_mag)
            VALUES (1, (SELECT AVG(mag) FROM earthquakes));
            """)
            cursor.execute("""
            INSERT OR REPLACE INTO latest_earthquake (id, time_utc, mag, place, longitude, latitude, depth_km, time_utc_human)
            SELECT id, time_utc, mag, place, longitude, latitude, depth_km, time_utc_human
            FROM earthquakes
            ORDER BY time_utc DESC
            LIMIT 1;
            """)
            cursor.execute("""
            INSERT OR REPLACE INTO max_mag (id, max_mag, place, time_utc, time_utc_human)
            SELECT id, MAX(mag), place, time_utc, time_utc_human
            FROM earthquakes;
            """)

            conn.commit()
            print(f"✅ Aggregates updated for chunk {current.date()} → {next_chunk.date()}.")

        current = next_chunk

    conn.close()
    print("✅ Historical seeding complete.")

if __name__ == "__main__":
    seed_historical_data()
