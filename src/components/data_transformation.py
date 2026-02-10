import sys
import os
import pandas as pd
from src.utils import push_to_feature_store  # Import our Mongo function

class DataTransformation:
    def initiate_data_transformation(self, data_path):
        print("Starting Feature Engineering...")
        try:
            # Read Raw Data
            df = pd.read_csv(data_path)
            
            # Ensure Date parsing (Handle Yahoo's format)
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)
            elif 'Datetime' in df.columns:
                 df['Datetime'] = pd.to_datetime(df['Datetime'])
                 df.set_index('Datetime', inplace=True)

            # Apply Feature Engineering (The Recipe)
            # Create Moving Averages
            df['SMA_10'] = df['Close'].rolling(window=10).mean()
            df['SMA_50'] = df['Close'].rolling(window=50).mean()
            
            # Create Volatility
            df['Volatility'] = df['Close'].rolling(window=10).std()
            
            # Create Target (Tomorrow's Price)
            df['Target'] = df['Close'].shift(-1)
            
            # Drop NaNs created by rolling windows
            df.dropna(inplace=True)

            # Push to MongoDB (Feature Store)
            # We push the CLEAN data so the Trainer can pull it later
            push_to_feature_store(df)
            
            print("Data Transformation & Feature Store Push Complete.")

        except Exception as e:
            raise Exception(e)