from Network_security.components.data_ingestion import NetworkDataextract
from Network_security.entity.config_entity import DataIngestionConfig, DataValidationConfig
from Network_security.entity.config_entity import TrainingPipelineConfig
from Network_security.components.data_validation import DataValidation
from Network_security.logger.logger import logging
from Network_security.Myexception.Myexception import CustomException
import sys


try:
    tconfig_obj = TrainingPipelineConfig()
    config_obj = DataIngestionConfig(tconfig_obj)
    ingestion_obj = NetworkDataextract(config_obj)
    res = ingestion_obj.initiate_data_ingestion()
    val_config_obj = DataValidationConfig(tconfig_obj)
    validation_obj = DataValidation(val_config_obj, res)
    val_res = validation_obj.validate_data()
    print(val_res)
    print(res)
except Exception as e:
    raise CustomException(e, sys) from e