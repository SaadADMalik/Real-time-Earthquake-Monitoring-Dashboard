## Overview

This project provides a real-time earthquake monitoring dashboard that fetches earthquake data from the USGS API every hour, stores it in a local SQLite database, and displays key information about the latest earthquakes, including their magnitudes, locations, and depths.

The data is visualized through a Power BI dashboard, where users can monitor various earthquake metrics such as total counts, average magnitudes, and the most recent and largest earthquakes.

### Features:
- Fetch earthquake data every hour from the [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/query).
- Store earthquake data in a local SQLite database.
- Aggregate and update earthquake statistics (e.g., total count, average magnitude, latest earthquake).
- Simple, yet effective, visualization of earthquake data using Power BI.

  ![Real-Time Earthquake Monitoring Dashboard](https://github.com/user-attachments/assets/ba7c9ac8-4b04-4c0c-978e-de074aa5de26)


## Getting Started

### Prerequisites

Ensure that you have the following installed on your system:
- Python 3.x
- SQLite3 (comes pre-installed with Python)
- Pandas (for handling data)
- Power BI (for dashboard visualization)


# How It Works
Fetching Data
The ingest.py script fetches earthquake data from the USGS Earthquake API every hour. The API response is parsed and stored in the earthquakes.db SQLite database.

# Database
The database contains the following tables:

earthquakes: Stores individual earthquake records with their respective magnitudes, locations, and timestamps.

avg_mag: Stores the average magnitude of all earthquakes.

total_earthquakes: Stores the total count of earthquakes.

latest_earthquake: Stores the most recent earthquake.

max_mag: Stores the maximum earthquake magnitude along with its location.

# Power BI Dashboard
The data from the SQLite database is visualized in Power BI, where you can see:

Total number of earthquakes

Average earthquake magnitude

Latest earthquake information

Maximum earthquake magnitude

# Alarm System (Future Work)
In the future, an alarm system will be integrated to notify users when significant earthquakes occur (e.g., magnitude greater than 5.0). Notifications can be sent via email, SMS, or other means.

File Descriptions
setup_db.py: Initializes the SQLite database and creates the required tables.

seed_2024_onward.py: Seeds historical earthquake data into the database from January 2024 onward.

ingest.py: Fetches real-time earthquake data every hour and inserts it into the database.

power_bi_dashboard.pbix: Power BI dashboard file for visualizing earthquake data.


# Acknowledgements
The USGS Earthquake API provides reliable real-time earthquake data.

Pandas for handling and processing earthquake data.

Power BI for visualizing earthquake data.

