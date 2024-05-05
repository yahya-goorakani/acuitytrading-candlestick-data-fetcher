# Candle Data Fetcher

This Python script fetches candle data from an external API, processes it, and stores it in a PostgreSQL database. It's built using Flask for the API endpoints and psycopg2 for interacting with the PostgreSQL database.

## Prerequisites

- Python 3.x installed
- PostgreSQL installed and running
- Flask and psycopg2 Python packages installed (`pip install Flask psycopg2 requests`)

## Configuration

1. Ensure that you have a PostgreSQL database set up.
2. Configure your PostgreSQL database credentials in the `config.py` file.
3. Update the API key in the `CandleData` class if necessary.

## Usage

1. Run the Flask application by executing `python Website.py`.
2. Access the `/fetch_data` endpoint to start fetching candle data.
3. Candle data will be fetched for different granularities (M: Minute, D: Day, W: Week, M: Month) with specified sleep times between each fetch.
4. The fetched data will be stored in PostgreSQL tables named `candles_<granularity>`.

## API Endpoints

- `/fetch_data`: Starts fetching candle data. This endpoint initiates the data fetching process for various granularities and sleep times.

## Structure

- `config.py`: Contains configuration parameters for connecting to the PostgreSQL database.
- `Website.py`: Main Flask application file containing the script to fetch and store candle data.
- `README.md`: Documentation file explaining the usage and structure of the project.
- `requirements.txt`: Lists the required Python packages for easy installation.

## Notes

- Ensure that your PostgreSQL database is properly configured and accessible.
- Handle errors gracefully, especially during database connections and data insertion.
- Make sure to keep your API key secure and avoid committing it to version control systems.
