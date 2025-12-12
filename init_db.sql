CREATE TABLE IF NOT EXISTS stock_data (
    symbol TEXT,
    date DATE,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume BIGINT,
    PRIMARY KEY (symbol, date)
);
