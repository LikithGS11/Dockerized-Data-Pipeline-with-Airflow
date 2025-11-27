# 📊 Dockerized Data Pipeline with Apache Airflow

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)](https://airflow.apache.org)

A production-ready, Dockerized ETL data pipeline that automatically fetches, processes, and stores stock market data from Alpha Vantage API into PostgreSQL using Apache Airflow orchestration.

## 🏗️ Architecture Overview

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

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Running the Pipeline](#running-the-pipeline)
- [Monitoring & Logs](#monitoring--logs)
- [Database Schema](#database-schema)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## ✅ Prerequisites

- **Docker**: Version 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: Version 2.0+ (included with Docker Desktop)
- **Alpha Vantage API Key**: Free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/LikithGS11/Dockerized-Data-Pipeline-with-Airflow.git
   cd Dockerized-Data-Pipeline-with-Airflow
   ```

2. **Get your API key**
   - Sign up at [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
   - Copy your free API key

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and replace YOUR_API_KEY_HERE with your actual API key
   ```

4. **Launch the pipeline**
   ```bash
   docker-compose up --build -d
   ```

5. **Access Airflow UI**
   - URL: http://localhost:8080
   - Username: `airflow`
   - Password: `airflow`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Airflow Configuration
AIRFLOW__CORE__EXECUTOR=CeleryExecutor
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
AIRFLOW__CORE__FERNET_KEY=46BKJoQYlPPOexq0OhDZnIlNepKFf87WFwLbfzqDDho=
AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=True
AIRFLOW__CORE__LOAD_EXAMPLES=False
AIRFLOW__WEBSERVER__RBAC=False
AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL=5
AIRFLOW__API__AUTH_BACKENDS=airflow.api.auth.backend.basic_auth
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow

# Database Configuration
POSTGRES_DB=airflow
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# API Configuration
API_KEY=your_alpha_vantage_api_key_here
```

### Default Credentials

- **Airflow Web UI**: `airflow` / `airflow`
- **PostgreSQL**: `airflow` / `airflow` (host: `localhost`, port: `5432`)

## 🎯 Running the Pipeline

### 1. Start Services
```bash
docker-compose up --build -d
```

### 2. Verify Services
```bash
docker-compose ps
```

### 3. Enable DAG
1. Open http://localhost:8080
2. Navigate to **DAGs** → Find `stock_pipeline`
3. Toggle the DAG to **ON**

### 4. Trigger Manual Run (Optional)
- Click the ▶️ button next to the DAG
- Or use CLI: `docker-compose exec airflow-worker airflow dags trigger stock_pipeline`

## 📊 Monitoring & Logs

### Airflow Web UI
- **URL**: http://localhost:8080
- **DAG Runs**: Monitor execution status and logs
- **Task Instances**: View individual task performance

### Container Logs
```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f airflow-worker
docker-compose logs -f postgres
```

### Database Inspection
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U airflow -d airflow

# Check data
SELECT COUNT(*) FROM stock_data;
SELECT * FROM stock_data LIMIT 5;
```

## 🗄️ Database Schema

The pipeline creates a `stock_data` table with the following schema:

```sql
CREATE TABLE IF NOT EXISTS stock_data (
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

### Sample Data Structure
```json
{
  "symbol": "IBM",
  "date": "2024-01-15",
  "open": 185.92,
  "high": 187.34,
  "low": 184.63,
  "close": 186.27,
  "volume": 3456789
}
```

## 🔧 Customization

### Change Stock Symbol
Edit `scripts/fetch_stock_data.py`:
```python
# Change this line
symbol = "IBM"  # Change to desired symbol (e.g., "AAPL", "GOOGL")
```

### Modify Schedule
Edit `dags/stock_pipeline_dag.py`:
```python
# Change schedule interval
dag = DAG(
    'stock_pipeline',
    default_args=default_args,
    description='Daily stock data pipeline',
    schedule_interval='@daily',  # Change to '@hourly', '0 9 * * *', etc.
    # ...
)
```

### Add More Stocks
Modify the fetch script to iterate over multiple symbols:
```python
symbols = ["IBM", "AAPL", "GOOGL", "MSFT"]
for symbol in symbols:
    fetch_and_store_stock_data(symbol)
```

## 🔍 Troubleshooting

### Common Issues

**1. DAG Not Appearing**
- Wait 30-60 seconds after startup
- Check Airflow scheduler logs: `docker-compose logs airflow-scheduler`

**2. API Rate Limits**
- Alpha Vantage free tier: 5 calls/minute, 500 calls/day
- Consider upgrading to premium for higher limits

**3. Database Connection Errors**
```bash
# Reset database
docker-compose down -v
docker-compose up --build -d
```

**4. Port Conflicts**
- Change ports in `docker-compose.yml` if 8080/5432 are in use

### Health Checks
```bash
# Check service health
docker-compose ps

# Test API connectivity
curl "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=YOUR_API_KEY"
```

## 💻 Development

### Local Development Setup
```bash
# Install dependencies (if running outside Docker)
pip install requests psycopg2-binary

# Run tests
python -m pytest tests/
```

### Project Structure
```
├── dags/
│   └── stock_pipeline_dag.py    # Airflow DAG definition
├── scripts/
│   └── fetch_stock_data.py      # Data fetching logic
├── docker-compose.yml           # Service orchestration
├── init_db.sql                  # Database initialization
├── .env                         # Environment variables
└── README.md                    # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Apache Airflow](https://airflow.apache.org/) - Workflow orchestration
- [Alpha Vantage](https://www.alphavantage.co/) - Stock market data API
- [PostgreSQL](https://postgresql.org/) - Database
- [Docker](https://docker.com/) - Containerization

---

**⭐ Star this repo if you found it helpful!**
