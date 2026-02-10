from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTrainer

if __name__ == "__main__":
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