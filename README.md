# Fetch Data to PostgreSQL Database

This Python script fetches candlestick data from the Acuity Trading API and stores it in a PostgreSQL database.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- `psycopg2` Python package for PostgreSQL database connection
- `requests` Python package for making HTTP requests

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/your_repository.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your_repository
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Update the `config.py` file with your PostgreSQL database connection parameters.

```python
# config.py

def config():
    params = {
        'dbname': 'your_database_name',
        'user': 'your_database_user',
        'password': 'your_database_password',
        'host': 'your_database_host',
        'port': 'your_database_port'
    }
    return params

##Usage

python fetch_data_to_db.py
