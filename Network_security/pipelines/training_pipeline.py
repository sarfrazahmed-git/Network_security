import sys
from Network_security.components.data_ingestion import NetworkDataextract
from Network_security.entity.config_entity import DataIngestionConfig, DataValidationConfig, TrainingPipelineConfig, DataTrainerConfig,DataTransformationConfig
from Network_security.components.data_validation import DataValidation
from Network_security.logger.logger import logging
from Network_security.Myexception.Myexception import CustomException
from Network_security.components.data_tranformer import DataTransformer
from Network_security.components.model_trainer import ModelTrainer




class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
        self.data_validation_config = DataValidationConfig(self.training_pipeline_config)
        self.data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
        self.data_trainer_config = DataTrainerConfig(self.training_pipeline_config)
    
    def start_data_ingestion(self):
        try:
            ingestion_obj = NetworkDataextract(self.data_ingestion_config)
            data_ingestion_artifact = ingestion_obj.initiate_data_ingestion()
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(f"Error in Data Ingestion: {e}", sys) from e
    def start_data_validation(self, data_ingestion_artifact):
        try:
            validation_obj = DataValidation(self.data_validation_config, data_ingestion_artifact)
            data_validation_artifact = validation_obj.validate_data()
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise CustomException(f"Error in Data Validation: {e}", sys) from e
    def start_data_transformation(self, data_validation_artifact):
        try:
            transformer_obj = DataTransformer(data_validation_artifact, self.data_transformation_config)
            data_transformation_artifact = transformer_obj.initiate_data_transformation()
            logging.info(f"Data Transformation Artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(f"Error in Data Transformation: {e}", sys) from e
    def start_model_training(self, data_transformation_artifact):
        try:
            model_trainer = ModelTrainer(self.data_trainer_config, data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(f"Error in Model Training: {e}", sys) from e
    def initiate_training_pipeline(self):
        try:
            logging.info("Starting Training Pipeline")
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_training(data_transformation_artifact)
            logging.info("Training Pipeline completed successfully")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(f"Error in Training Pipeline: {e}", sys) from e