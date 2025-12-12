# Dockerized Data Pipeline with Apache Airflow

A production-ready ETL pipeline that automatically fetches stock market data from Alpha Vantage API and stores it in PostgreSQL using Apache Airflow orchestration.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Alpha Vantage  │───▶│   Apache Airflow  │───▶│   PostgreSQL    │
│      API        │    │     (Celery)      │    │    Database     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │     Redis        │
                       │   (Message Queue)│
                       └──────────────────┘
```

The pipeline uses Docker containers for Airflow scheduler, worker, webserver, PostgreSQL database, and Redis message broker.

## Features

- **Automated ETL workflow** – Scheduled data extraction, transformation, and loading
- **Dockerized deployment** – Fully containerized with Docker Compose
- **Celery executor** – Distributed task execution with Redis queue
- **Daily scheduling** – Automatic daily stock data updates
- **Web UI monitoring** – Real-time pipeline monitoring via Airflow UI
- **PostgreSQL storage** – Structured data storage with schema enforcement

## Tech Stack

- **Apache Airflow** (v2.x) with CeleryExecutor
- **PostgreSQL** (v13) for data storage
- **Redis** for message brokering
- **Docker & Docker Compose** for containerization
- **Alpha Vantage API** for stock market data

## Prerequisites

- Docker 20.10+ and Docker Compose 2.0+
- Alpha Vantage API key (free at [alphavantage.co](https://www.alphavantage.co/support/#api-key))

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/LikithGS11/Dockerized-Data-Pipeline-with-Airflow.git
   cd Dockerized-Data-Pipeline-with-Airflow
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Alpha Vantage API key:
   ```env
   API_KEY=your_alpha_vantage_api_key_here
   ```

3. **Launch services**:
   ```bash
   docker-compose up --build -d
   ```

4. **Access Airflow UI**:
   - URL: http://localhost:8080
   - Username: `airflow`
   - Password: `airflow`

5. **Enable the DAG**:
   - Navigate to the `stock_pipeline` DAG
   - Toggle it to **ON**

## Configuration

### Environment Variables

Key configuration in `.env` file:

```env
# Airflow
AIRFLOW__CORE__EXECUTOR=CeleryExecutor
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0

# Database
POSTGRES_DB=airflow
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow

# API
API_KEY=your_alpha_vantage_api_key_here
```

### Default Credentials

- **Airflow UI**: `airflow` / `airflow`
- **PostgreSQL**: `airflow` / `airflow` (port: 5432)

## Project Structure

```
├── dags/
│   └── stock_pipeline_dag.py    # DAG definition
├── scripts/
│   └── fetch_stock_data.py      # Data fetching logic
├── docker-compose.yml           # Service orchestration
├── init_db.sql                  # Database schema
├── .env                         # Environment variables
└── README.md
```

## Database Schema

The pipeline creates a `stock_data` table:

```sql
CREATE TABLE stock_data (
    symbol TEXT NOT NULL,
    date DATE NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume BIGINT,
    PRIMARY KEY (symbol, date)
);
```

## Monitoring

### Airflow Web UI
- **DAG Runs**: Monitor execution status and history
- **Task Logs**: View detailed task execution logs
- **URL**: http://localhost:8080

### Container Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f airflow-worker
```

### Database Inspection
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U airflow -d airflow

# Query data
SELECT COUNT(*) FROM stock_data;
SELECT * FROM stock_data LIMIT 10;
```

## Customization

### Change Stock Symbol
Edit `scripts/fetch_stock_data.py`:
```python
symbol = "AAPL"  # Change to any valid symbol
```

### Modify Schedule
Edit `dags/stock_pipeline_dag.py`:
```python
schedule_interval='@daily'  # Options: '@hourly', '0 9 * * *', etc.
```

### Add Multiple Stocks
Update the fetch script to process multiple symbols:
```python
symbols = ["IBM", "AAPL", "GOOGL", "MSFT"]
for symbol in symbols:
    fetch_and_store_stock_data(symbol)
```

## Troubleshooting

### DAG Not Visible
- Wait 30-60 seconds after startup for Airflow to scan DAGs
- Check scheduler logs: `docker-compose logs airflow-scheduler`

### API Rate Limits
- Free tier: 5 calls/minute, 500 calls/day
- Space out requests or upgrade to premium

### Database Connection Errors
```bash
# Reset all services and volumes
docker-compose down -v
docker-compose up --build -d
```

### Port Conflicts
If ports 8080 or 5432 are in use, modify them in `docker-compose.yml`.

## Commands Reference

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart service
docker-compose restart airflow-worker

# Trigger DAG manually
docker-compose exec airflow-worker airflow dags trigger stock_pipeline

# List DAGs
docker-compose exec airflow-worker airflow dags list
```
## API Rate Limits

Alpha Vantage free tier limits:
- 5 API calls per minute
- 500 API calls per day
Adjust your schedule accordingly or consider premium plans for higher limits.

---
