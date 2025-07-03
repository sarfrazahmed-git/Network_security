from Network_security.components.data_ingestion import NetworkDataextract
from Network_security.entity.config_entity import DataIngestionConfig
from Network_security.entity.config_entity import TrainingPipelineConfig
tconfig_obj = TrainingPipelineConfig()
config_obj = DataIngestionConfig(tconfig_obj)
ingestion_obj = NetworkDataextract(config_obj)
res = ingestion_obj.initiate_data_ingestion()
print(res)