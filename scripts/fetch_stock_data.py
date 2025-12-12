import requests
import psycopg2
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_and_store_stock_data():
    # API configuration
    api_key = os.getenv('API_KEY')
    symbol = 'IBM'  # You can make this configurable
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'

    try:
        # Fetch data from API
        logger.info(f"Fetching data for symbol: {symbol}")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Check for API errors
        if 'Error Message' in data:
            raise ValueError(f"API Error: {data['Error Message']}")

        if 'Time Series (Daily)' not in data:
            raise ValueError("No time series data found in API response")

        # Parse the data
        time_series = data['Time Series (Daily)']
        records = []

        for date_str, daily_data in time_series.items():
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                open_price = float(daily_data['1. open'])
                high_price = float(daily_data['2. high'])
                low_price = float(daily_data['3. low'])
                close_price = float(daily_data['4. close'])
                volume = int(daily_data['5. volume'])

                records.append((symbol, date, open_price, high_price, low_price, close_price, volume))
            except (ValueError, KeyError) as e:
                logger.warning(f"Error parsing data for date {date_str}: {e}")
                continue

        if not records:
            raise ValueError("No valid records to insert")

        # Database connection
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'),
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        cursor = conn.cursor()

        # Insert data (use ON CONFLICT to handle duplicates)
        insert_query = """
        INSERT INTO stock_data (symbol, date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (symbol, date) DO NOTHING
        """

        cursor.executemany(insert_query, records)
        conn.commit()

        logger.info(f"Successfully inserted {cursor.rowcount} records")

    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise
    except ValueError as e:
        logger.error(f"Data processing error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
