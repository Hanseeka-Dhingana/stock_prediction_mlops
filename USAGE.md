# Data Ingestion Module - Usage Guide

This guide explains how to use the `data_ingestion.py` module for fetching and processing stock market data.

## Overview

The data ingestion module provides functionality to:
- Fetch historical stock data from Yahoo Finance (via yfinance)
- Validate data quality (check for missing values, negative prices, etc.)
- Save data to local storage for further processing
- Generate summary statistics

## Prerequisites

Install required dependencies:
```bash
pip install yfinance pandas
```

## Basic Usage

### Example 1: Fetch and Save Stock Data

```python
from src.components.data_ingestion import DataIngestionConfig, DataIngestion

# Create configuration
config = DataIngestionConfig(
    stock_symbol="AAPL",           # Stock ticker symbol
    start_date="2023-01-01",       # Start date (YYYY-MM-DD)
    end_date="2024-01-01",         # End date (YYYY-MM-DD)
    raw_data_path="artifacts/data/raw"  # Output directory
)

# Initialize and run ingestion
ingestion = DataIngestion(config)
df, filepath = ingestion.ingest()

print(f"Data saved to: {filepath}")
print(df.head())
```

### Example 2: Using Default Configuration

```python
from src.components.data_ingestion import DataIngestionConfig, DataIngestion

# Use defaults (AAPL stock, last 1 year)
config = DataIngestionConfig()
ingestion = DataIngestion(config)
df, filepath = ingestion.ingest()
```

### Example 3: Fetch Multiple Stocks

```python
from src.components.data_ingestion import DataIngestionConfig, DataIngestion

stocks = ["AAPL", "GOOGL", "MSFT", "TSLA"]

for symbol in stocks:
    config = DataIngestionConfig(
        stock_symbol=symbol,
        start_date="2023-01-01",
        end_date="2024-01-01"
    )
    ingestion = DataIngestion(config)
    df, filepath = ingestion.ingest()
    print(f"Processed {symbol}: {filepath}")
```

### Example 4: Custom Data Processing

```python
from src.components.data_ingestion import DataIngestionConfig, DataIngestion

config = DataIngestionConfig(stock_symbol="AAPL")
ingestion = DataIngestion(config)

# Fetch data
df = ingestion.fetch_stock_data()

# Validate data
ingestion.validate_data(df)

# Get summary statistics
summary = ingestion.get_data_summary(df)
print(f"Summary: {summary}")

# Save with custom filename
filepath = ingestion.save_data(df, filename="my_custom_data.csv")
```

## Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `raw_data_path` | str | "artifacts/data/raw" | Directory to save raw data |
| `stock_symbol` | str | "AAPL" | Stock ticker symbol |
| `start_date` | str | 1 year ago | Start date (YYYY-MM-DD format) |
| `end_date` | str | Today | End date (YYYY-MM-DD format) |
| `interval` | str | "1d" | Data interval (1d, 1h, etc.) |

## Data Validation

The module performs the following validations:
- ✅ Checks for required columns (Open, High, Low, Close, Volume)
- ✅ Validates no negative prices
- ✅ Ensures High >= Low
- ✅ Checks Close is within High-Low range
- ✅ Reports missing/null values
- ✅ Validates data types

## Output Format

Data is saved as CSV with the following structure:
```
Date,Open,High,Low,Close,Volume
2023-01-01,100.0,105.0,95.0,102.0,1000000
2023-01-02,102.0,106.0,96.0,103.0,1100000
...
```

## Error Handling

The module handles various error scenarios:
- Network errors when fetching data
- Invalid stock symbols
- Data validation failures
- File system errors

All errors are logged with appropriate messages.

## Logging

The module uses Python's logging framework:
```python
import logging

# Set logging level
logging.basicConfig(level=logging.DEBUG)
```

## Integration with MLOps Pipeline

This module is designed to be the first step in an MLOps pipeline:

1. **Data Ingestion** (this module) → Fetch and validate raw data
2. **Data Transformation** → Process and feature engineering
3. **Model Training** → Train ML models
4. **Model Evaluation** → Evaluate model performance
5. **Model Deployment** → Deploy to production

## Next Steps

After data ingestion, the data can be passed to:
- `data_transformation.py` for feature engineering
- `model_training.py` for model training
- Direct analysis and visualization

## Common Issues

### ImportError: No module named 'yfinance'
**Solution:** Install yfinance: `pip install yfinance`

### Network Error
**Solution:** Check internet connection and firewall settings

### Empty DataFrame
**Solution:** Verify stock symbol is correct and date range is valid

## Advanced Usage

### Custom Validation

```python
from src.components.data_ingestion import DataIngestion

class CustomDataIngestion(DataIngestion):
    def validate_data(self, df):
        # Call parent validation
        super().validate_data(df)
        
        # Add custom validation
        if df['Volume'].mean() < 100000:
            raise ValueError("Average volume too low")
        
        return True
```

## Support

For issues or questions, please refer to the main project documentation or raise an issue in the repository.
