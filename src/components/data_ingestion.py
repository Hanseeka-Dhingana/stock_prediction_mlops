import os
import sys
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
        print("Checking Data Source...")
        
        # check does the file already exist?
        if os.path.exists(self.ingestion_config.raw_data_path):
            print(f"Data already exists at {self.ingestion_config.raw_data_path}")
            print("   Skipping download to save time.")
            return self.ingestion_config.raw_data_path
        
        # if not exist then download and create folder
        print("   Data not found. Downloading from Yahoo Finance...")
        try:
            # Download Data
            df = yf.download("GOOGL", start="2020-01-01", end="2026-01-01")
            
            # Create folder if missing
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            
            # Save Raw Data
            df.to_csv(self.ingestion_config.raw_data_path)
            print(f"Download complete! Saved to {self.ingestion_config.raw_data_path}")
            
            return self.ingestion_config.raw_data_path

        except Exception as e:
            raise Exception(e)

if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()