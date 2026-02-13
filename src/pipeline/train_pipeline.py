import wandb
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTrainer
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("WANDB_API_KEY")

if api_key:
    print(f"✅ Found WANDB_API_KEY (Length: {len(api_key)})")
    # 3. FORCE LOGIN
    wandb.login(key=api_key)
else:
    print("❌ ERROR: WANDB_API_KEY is missing or empty in .env!")
    print("   Please check your .env file location.")

if __name__ == "__main__":
    
    # Check if the key loaded correctly (Optional debugging)

    
    # INGESTION
    # Checks for file or downloads it
    ingestion_obj = DataIngestion()
    raw_data_path = ingestion_obj.initiate_data_ingestion()

    # TRANSFORMATION
    # Reads raw data -> Engineers Features -> Pushes to MongoDB
    transform_obj = DataTransformation()
    transform_obj.initiate_data_transformation(raw_data_path)

    # TRAINING
    # Pulls from MongoDB -> Trains -> Saves Model
    trainer_obj = ModelTrainer()
    trainer_obj.initiate_model_trainer()