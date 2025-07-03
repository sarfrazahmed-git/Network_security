import numpy as np
from Network_security.entity.config_entity import DataIngestionConfig
from Network_security.entity.artifact_entity import ArtifactEntity
from Network_security.logger.logger import logging
from Network_security.Myexception.Myexception import CustomException

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import sys
import dotenv
import certifi
import pandas as pd
import json
from sklearn.model_selection import train_test_split
dotenv.load_dotenv(dotenv.find_dotenv())
url = os.getenv("MONGO_DB_URL")
ca = certifi.where()

class NetworkDataextract:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        self.client = MongoClient(url, server_api=ServerApi("1"), tlsCAFile=ca)
        self.db = self.client[data_ingestion_config.database_name]
        self.collection = self.db[data_ingestion_config.collection_name]
    def read_from_mongo(self):
        try:
            records = list(self.collection.find({}))
            if not records:
                raise CustomException("No data found in the collection", sys)
            df = pd.DataFrame(records)
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True, axis=1)
            df.replace({"na":np.nan}, inplace=True)
            return df
        except Exception as e:
            raise CustomException(e, sys)
    
    def store_to_feature_store(self, df: pd.DataFrame):
        os.makedirs(self.data_ingestion_config.feature_store_dir, exist_ok=True)
        feature_store_path = os.path.join(self.data_ingestion_config.feature_store_dir, "feature_store.csv")
        try:
            df.to_csv(feature_store_path, index=False)
            logging.info(f"Feature store created at {feature_store_path}")
            return pd.read_csv(feature_store_path)
        except Exception as e:
            raise CustomException(e, sys)
    def split_train_test(self, df: pd.DataFrame):
        try:
            train_df, test_df = train_test_split(
                df, 
                test_size=self.data_ingestion_config.train_test_split_ratio, 
                random_state=42
            )
            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Train and test data split with ratio {self.data_ingestion_config.train_test_split_ratio}")
            logging.info(f"Train data shape: {train_df.shape}, Test data shape: {test_df.shape}")
            dir_path = os.path.dirname(self.data_ingestion_config.test_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Train and test data directories created at {dir_path}")
            train_df.to_csv(self.data_ingestion_config.train_file_path, index=False)
            test_df.to_csv(self.data_ingestion_config.test_file_path, index=False)
            logging.info(f"Train and test data saved to {self.data_ingestion_config.train_file_path} and {self.data_ingestion_config.test_file_path}")
            return train_df, test_df
        except Exception as e:
            raise CustomException(e, sys)
    def initiate_data_ingestion(self):
        try:
            df = self.read_from_mongo()
            df = self.store_to_feature_store(df)
            logging.info("Data read from MongoDB and stored in feature store.")
            self.split_train_test(df)
            result = ArtifactEntity(train_file_path = self.data_ingestion_config.train_file_path,
                            test_file_path = self.data_ingestion_config.test_file_path)
            logging.info("Data ingestion completed successfully.")
            return result

        except Exception as e:
            raise CustomException(e, sys)
    

