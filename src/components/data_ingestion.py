"""
Data Ingestion Module for Stock Prediction MLOps Project

This module handles fetching stock market data from various sources,
validates the data quality, and stores it for further processing.
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataIngestionConfig:
    """Configuration class for data ingestion parameters."""
    
    def __init__(
        self,
        raw_data_path: str = "artifacts/data/raw",
        stock_symbol: str = "AAPL",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        interval: str = "1d"
    ):
        """
        Initialize data ingestion configuration.
        
        Args:
            raw_data_path: Directory path to store raw data
            stock_symbol: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
            start_date: Start date for data fetching (YYYY-MM-DD)
            end_date: End date for data fetching (YYYY-MM-DD)
            interval: Data interval (1d, 1h, etc.)
        """
        self.raw_data_path = raw_data_path
        self.stock_symbol = stock_symbol
        self.interval = interval
        
        # Set default dates if not provided
        if end_date is None:
            self.end_date = datetime.now().strftime('%Y-%m-%d')
        else:
            self.end_date = end_date
            
        if start_date is None:
            # Default to 1 year of historical data
            self.start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        else:
            self.start_date = start_date
        
        # Create directory if it doesn't exist
        os.makedirs(self.raw_data_path, exist_ok=True)


class DataIngestion:
    """
    Main class for ingesting stock market data.
    
    This class provides methods to:
    - Fetch stock data from yfinance API
    - Validate data quality
    - Save data to local storage
    """
    
    def __init__(self, config: DataIngestionConfig):
        """
        Initialize DataIngestion with configuration.
        
        Args:
            config: DataIngestionConfig object with ingestion parameters
        """
        self.config = config
        logger.info(f"Initialized DataIngestion for {config.stock_symbol}")
        
    def fetch_stock_data(self) -> pd.DataFrame:
        """
        Fetch stock data from yfinance API.
        
        Returns:
            DataFrame containing stock data with OHLCV columns
            
        Raises:
            Exception: If data fetching fails
        """
        try:
            logger.info(
                f"Fetching data for {self.config.stock_symbol} "
                f"from {self.config.start_date} to {self.config.end_date}"
            )
            
            # Try to import yfinance
            try:
                import yfinance as yf
            except ImportError:
                logger.error(
                    "yfinance library not found. Please install it using: "
                    "pip install yfinance"
                )
                raise ImportError(
                    "yfinance is required for data ingestion. "
                    "Install it with: pip install yfinance"
                )
            
            # Fetch data using yfinance
            ticker = yf.Ticker(self.config.stock_symbol)
            df = ticker.history(
                start=self.config.start_date,
                end=self.config.end_date,
                interval=self.config.interval
            )
            
            if df.empty:
                raise ValueError(
                    f"No data retrieved for {self.config.stock_symbol}. "
                    "Please check the symbol and date range."
                )
            
            logger.info(f"Successfully fetched {len(df)} rows of data")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching stock data: {str(e)}")
            raise
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Validate the quality of fetched stock data.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if validation passes, False otherwise
            
        Raises:
            ValueError: If critical validation checks fail
        """
        logger.info("Validating stock data...")
        
        # Check if dataframe is empty
        if df.empty:
            raise ValueError("DataFrame is empty")
        
        # Check for required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Check for null values
        null_counts = df[required_columns].isnull().sum()
        if null_counts.any():
            logger.warning(f"Found null values in columns:\n{null_counts[null_counts > 0]}")
            # Log percentage of nulls
            for col in required_columns:
                null_pct = (df[col].isnull().sum() / len(df)) * 100
                if null_pct > 0:
                    logger.warning(f"{col}: {null_pct:.2f}% null values")
        
        # Check for negative values in price columns
        price_columns = ['Open', 'High', 'Low', 'Close']
        for col in price_columns:
            if (df[col] < 0).any():
                logger.error(f"Found negative values in {col} column")
                raise ValueError(f"Invalid negative values found in {col}")
        
        # Check for negative volume
        if (df['Volume'] < 0).any():
            logger.error("Found negative values in Volume column")
            raise ValueError("Invalid negative values found in Volume")
        
        # Check High-Low relationship
        if (df['High'] < df['Low']).any():
            logger.error("Found instances where High < Low")
            raise ValueError("Invalid data: High price is less than Low price")
        
        # Check if Close is within High-Low range
        invalid_close = ((df['Close'] > df['High']) | (df['Close'] < df['Low'])).sum()
        if invalid_close > 0:
            logger.warning(
                f"Found {invalid_close} instances where Close is outside High-Low range"
            )
        
        logger.info("Data validation completed successfully")
        return True
    
    def save_data(self, df: pd.DataFrame, filename: Optional[str] = None) -> str:
        """
        Save DataFrame to CSV file.
        
        Args:
            df: DataFrame to save
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.config.stock_symbol}_{timestamp}.csv"
        
        filepath = os.path.join(self.config.raw_data_path, filename)
        
        try:
            df.to_csv(filepath)
            logger.info(f"Data saved successfully to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            raise
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate summary statistics for the fetched data.
        
        Args:
            df: DataFrame to summarize
            
        Returns:
            Dictionary containing summary statistics
        """
        summary = {
            'symbol': self.config.stock_symbol,
            'total_records': len(df),
            'start_date': df.index.min().strftime('%Y-%m-%d'),
            'end_date': df.index.max().strftime('%Y-%m-%d'),
            'columns': list(df.columns),
            'null_counts': df.isnull().sum().to_dict(),
            'price_stats': {
                'mean_close': df['Close'].mean(),
                'max_high': df['High'].max(),
                'min_low': df['Low'].min(),
                'avg_volume': df['Volume'].mean()
            }
        }
        return summary
    
    def ingest(self) -> Tuple[pd.DataFrame, str]:
        """
        Main method to execute the complete data ingestion pipeline.
        
        This method:
        1. Fetches stock data
        2. Validates the data
        3. Saves the data to file
        4. Returns the DataFrame and file path
        
        Returns:
            Tuple of (DataFrame, filepath)
        """
        try:
            logger.info("Starting data ingestion pipeline...")
            
            # Fetch data
            df = self.fetch_stock_data()
            
            # Validate data
            self.validate_data(df)
            
            # Get and log summary
            summary = self.get_data_summary(df)
            logger.info(f"Data summary: {summary}")
            
            # Save data
            filepath = self.save_data(df)
            
            logger.info("Data ingestion pipeline completed successfully")
            return df, filepath
            
        except Exception as e:
            logger.error(f"Data ingestion pipeline failed: {str(e)}")
            raise


if __name__ == "__main__":
    """
    Example usage of DataIngestion class
    """
    # Create configuration
    config = DataIngestionConfig(
        stock_symbol="AAPL",
        start_date="2023-01-01",
        end_date="2024-01-01"
    )
    
    # Initialize and run ingestion
    ingestion = DataIngestion(config)
    df, filepath = ingestion.ingest()
    
    print(f"\nData ingestion completed!")
    print(f"Saved to: {filepath}")
    print(f"\nFirst few rows of data:")
    print(df.head())
