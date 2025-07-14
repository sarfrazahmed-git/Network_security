from Network_security.components.data_ingestion import NetworkDataextract
from Network_security.entity.config_entity import DataIngestionConfig, DataValidationConfig
from Network_security.entity.config_entity import TrainingPipelineConfig
from Network_security.components.data_validation import DataValidation
from Network_security.logger.logger import logging
from Network_security.Myexception.Myexception import CustomException
from Network_security.entity.config_entity import DataTransformationConfig
from Network_security.components.data_tranformer import DataTransformer
from Network_security.components.model_trainer import ModelTrainer
from Network_security.entity.config_entity import DataTrainerConfig
from Network_security.pipelines.training_pipeline import TrainingPipeline
import sys

if __name__ == "__main__":
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.initiate_training_pipeline()
    except Exception as e:
        raise CustomException(e, sys) from e
