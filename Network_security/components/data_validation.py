import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import  ks_2samp
from Network_security.entity.config_entity import DataValidationConfig
from Network_security.logger.logger import logging
from Network_security.Myexception.Myexception import CustomException
from Network_security.entity.artifact_entity import ArtifactEntity, DataValidationArtifact
from Network_security.util.validation_util.utils import read_yaml_file, write_yaml_file



class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: ArtifactEntity):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(self.data_validation_config.schema_file_path)
        except Exception as e:
            raise CustomException(e, sys) from e
    def validate_number_of_columns(self,df):
        try:
            num_colums = len(self._schema_config["columns"])
            num_available_columns = len(df.columns)
            if num_colums != num_available_columns:
                return False
            return True
        except Exception as e:
            raise CustomException(e, sys) from e
    def validate_columns(self, df):
        try:
            columns = df.columns
            d_types = df.dtypes
            print(self._schema_config['columns'])
            required_columns = []
            schema_dict = {}
            for dict in self._schema_config['columns']:
                for key, value in dict.items():
                    required_columns.append(key)
                    schema_dict[key] = value
            for column in required_columns:
                if column not in columns:
                    return False
                elif schema_dict[column] != str(d_types[column]):
                    return False
            return True
        except Exception as e:
            raise CustomException(e, sys) from e

    def detect_drift(self, base_df,current_df,threshold=0.05):
        try:
            status = True
            report = {}
            for column in base_df.columns:
                isfound = False
                d1 = base_df[column]
                d2 = current_df[column]
                is_sample_dist = ks_2samp(d1, d2)
                if is_sample_dist.pvalue < threshold:
                    isfound = True
                    status = False
                else:
                    isfound = False
                report.update({column: {"is_found": isfound, "p_value": is_sample_dist.pvalue}})
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            logging.info(f"Drift report generated at {report}")
            write_yaml_file(drift_report_file_path, report)
            return status


        except Exception as e:
            raise CustomException(e, sys) from e


    def write_validated_data(self,df, train:bool):
        try:
            if train:
                file_path = self.data_validation_config.validated_train_file_path
            else:
                file_path = self.data_validation_config.validated_test_file_path
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            df.to_csv(file_path, index=False)
        except Exception as e:
            raise CustomException(e, sys) from e

    def write_invalid_data(self, df, train: bool):
        try:
            if train:
                file_path = self.data_validation_config.invalid_train_file_path
            else:
                file_path = self.data_validation_config.invalid_test_file_path
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            df.to_csv(file_path, index=False)
        except Exception as e:
            raise CustomException(e, sys) from e

    def log_write_data(self,df,train:bool,statues, messages_keys, error_messages):
        try:
            validated = True
            for i in range(len(statues)):
                if statues[i] == False:
                    logging.error(f"Invalid train data: {error_messages[messages_keys[i]]}")
                    validated = False
            if validated:
                logging.info("Train data validation successful")
                self.write_validated_data(df, train)
            else:
                logging.error("Train data validation failed")
                self.write_invalid_data(df, train)

        except Exception as e:
            raise CustomException(e, sys) from e

    def validate_data(self):
        error_messages = {}
        df_train = pd.read_csv(self.data_ingestion_artifact.train_file_path)
        df_test = pd.read_csv(self.data_ingestion_artifact.test_file_path)
        train_len_status = self.validate_number_of_columns(df_train)
        
        if train_len_status == False:
            error_messages["train_length"] = f"Number of columns in train file {len(df_train.columns)} does not match schema {len(self._schema_config['columns'])}"
        train_col_status = self.validate_columns(df_train)
        if train_col_status == False:
            error_messages["train_columns"] = f"Columns in train file {df_train.columns} do not match schema {self._schema_config['columns'].keys()}"

        test_len_status = self.validate_number_of_columns(df_test)
        if test_len_status == False:
            error_messages["test_length"] = f"Number of columns in test file {len(df_test.columns)} does not match schema {len(self._schema_config['columns'])}"
        test_col_status = self.validate_columns(df_test)
        if test_col_status == False:
            error_messages["test_columns"] = f"Columns in test file {df_test.columns} do not match schema {self._schema_config['columns'].keys()}"

        drift_status = self.detect_drift(df_train, df_test)
        if drift_status == False:
            error_messages["data_drift"] = "Data drift detected between train and test files"



        status_train = [train_len_status, train_col_status, drift_status]
        message_key_train = ["train_length", "train_columns", "data_drift"]

        status_test = [test_len_status, test_col_status, drift_status]
        message_key_test = ["test_length", "test_columns", "data_drift"]

        self.log_write_data(df_train, True, status_train, message_key_train, error_messages)
        self.log_write_data(df_test, False, status_test, message_key_test, error_messages)
        logging.info("Data validation completed")

        return DataValidationArtifact(
            validation_status=not bool(error_messages),
            valid_train_file_path=self.data_validation_config.validated_train_file_path,
            valid_test_file_path=self.data_validation_config.validated_test_file_path,
            drift_report_file_path= self.data_validation_config.drift_report_file_path,
            invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
            invalid_test_file_path=self.data_validation_config.invalid_test_file_path
        )






    