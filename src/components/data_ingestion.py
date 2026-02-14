import os
import sys
import pandas as pd
import yfinance as yf
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    # Where to save the raw data
    raw_data_path: str = os.path.join('data', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        print("Starting Data Ingestion for Retraining...")
        


        try:
            print("Downloading latest data from Yahoo Finance...")
            
           
            # This get data up to TODAY, forever.
            df = yf.download("GOOGL", period="5y", interval="1d")
            
            # Formatting checks (MultiIndex handling)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Reset index so 'Date' becomes a column (Critical for Prophet/XGBoost)
            df.reset_index(inplace=True)

            # Create folder if missing
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            
            # Save Raw Data (Overwriting the old one)
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            
            print(f"Download complete! Fetched data up to {df['Date'].max()}")
            print(f"Saved to {self.ingestion_config.raw_data_path}")
            
            return self.ingestion_config.raw_data_path

        except Exception as e:
            raise Exception(f"Data Ingestion Failed: {e}")

if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()