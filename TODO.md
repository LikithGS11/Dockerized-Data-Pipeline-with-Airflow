# TODO List for Dockerized Data Pipeline

## Completed Tasks
- [x] Create README.md with setup and usage instructions
- [x] Create docker-compose.yml for Airflow, PostgreSQL, and Redis services
- [x] Create init_db.sql to initialize the stock_data table
- [x] Create scripts/fetch_stock_data.py with API fetching and database insertion logic
- [x] Create .env file with environment variables
- [x] Create dags/stock_pipeline_dag.py with the Airflow DAG definition
- [x] Obtain Alpha Vantage API key and update .env file

## Remaining Tasks
- [x] Run `docker-compose up --build -d` to start services (in progress)
- [ ] Access Airflow UI at http://localhost:8080 (username: airflow, password: airflow)
- [ ] Enable the stock_pipeline_dag in Airflow UI
- [ ] Trigger the DAG manually to test data fetching
- [ ] Verify data insertion in PostgreSQL database
- [ ] Test error handling with invalid API key or network issues
- [ ] Customize symbol, schedule, or add more features as needed
