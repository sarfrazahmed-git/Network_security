from datetime import datetime
import os
from Network_security.constant.training_pipeline import consts as training_pipeline
from Network_security.logger.logger import logging
from Network_security.Myexception.Myexception import CustomException


class TrainingPipelineConfig:
    def __init__(self,timestamp = datetime.now()):
        self.timestamp = timestamp
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(training_pipeline.ARTIFACT_DIR, str(self.timestamp))
        
class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME,
        )

        self.feature_store_dir = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR
        )

        self.train_file_path = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )
        self.test_file_path = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )
        self.database_name = training_pipeline.DATA_INGESTION_DB_NAME
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
