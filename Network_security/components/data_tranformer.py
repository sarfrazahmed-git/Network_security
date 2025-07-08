from Network_security.logger.logger import logging
from Network_security.Myexception.Myexception import CustomException

from Network_security.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from Network_security.entity.config_entity import DataTransformationConfig
from Network_security.constant.training_pipeline import consts as training_pipeline
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from Network_security.util.main_util.utils import save_object,save_numpy_array_data
import sys
import pandas as pd
import numpy as np



class DataTransformer:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def get_data_transformation_object(self):
        try:
            imputer_config = training_pipeline.DATA_TRANSFORMATION_IMPUTER_PARAMS
            imputer = KNNImputer(**imputer_config)
            pipeline = Pipeline(steps=[('imputer', imputer)])
            return pipeline
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def initiate_data_transformation(self):
        logging.info("Initiating data transformation")
        try:
            train_path = self.data_validation_artifact.valid_train_file_path
            test_path = self.data_validation_artifact.valid_test_file_path
            
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            train_features = train_df.drop(columns=[training_pipeline.TARGET_COLUMN])
            train_target = train_df[training_pipeline.TARGET_COLUMN]

            test_features = test_df.drop(columns=[training_pipeline.TARGET_COLUMN])
            test_target = test_df[training_pipeline.TARGET_COLUMN]

            train_target = train_target.replace(-1,0)
            test_target = test_target.replace(-1,0)

            data_transformation_object = self.get_data_transformation_object()
            transformed_train_features = data_transformation_object.fit_transform(train_features)
            transformed_test_features = data_transformation_object.transform(test_features)
            logging.info("Data transformation completed")

            train_arr = np.c_[transformed_train_features, train_target]
            test_arr = np.c_[transformed_test_features, test_target]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, data_transformation_object)

            ret_obj = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                data_transformation_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            logging.info(f"Data transformation artifact created: {ret_obj}")
            return ret_obj

        except Exception as e:
            raise CustomException(e, sys) from e