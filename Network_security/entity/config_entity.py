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

class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME
        )
        
        self.validated_train_file_path = os.path.join(
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALIDATED_DIR,training_pipeline.TRAIN_FILE_NAME
        )
        self.validated_test_file_path = os.path.join(
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALIDATED_DIR, training_pipeline.TEST_FILE_NAME
        )
        self.invalid_train_file_path = os.path.join(
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR, training_pipeline.TRAIN_FILE_NAME
        )
        self.invalid_test_file_path = os.path.join(
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR, training_pipeline.TEST_FILE_NAME
        )
        self.drift_report_file_path = os.path.join(
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )
        self.schema_file_path = training_pipeline.SCHEMA_FILE_PATH


class DataTransformationConfig:
     def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join( training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME )
        self.transformed_train_file_path: str = os.path.join( self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),)
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,  training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy"), )
        self.transformed_object_file_path: str = os.path.join( self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME,)

class DataTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.trained_model_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR
        )
        self.trained_model_file_path = os.path.join(
            self.trained_model_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME
        )
        self.expected_score = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.over_fitting_under_fitting_threshold = training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD