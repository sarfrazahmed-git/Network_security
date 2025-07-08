import yaml
from Network_security.Myexception.Myexception import CustomException
import sys
from Network_security.logger.logger import logging
import numpy as np
import pickle
import dill
import os
def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            content = yaml.safe_load(file)
        return content
    except Exception as e:
        raise CustomException(e, sys) from e

def sanitize(obj):
    if isinstance(obj,dict):
        return {k: sanitize(v) for k, v in obj.items()}
    elif isinstance(obj,list):
        return [sanitize(item) for item in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    
def write_yaml_file(file_path: str, content: dict):
    
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(sanitize(content), file)
    except Exception as e:
        raise CustomException(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.ndarray):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, array)
    except Exception as e:
        raise CustomException(e, sys) from e
    
def save_object(file_path: str, obj: object):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
                pickle.dump(obj, file)
    except Exception as e:
        raise CustomException(e, sys) from e
    
def load_object(file_path: str):
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        raise CustomException(e, sys) from e
    
def load_numpy_array_data(file_path: str):
    try:
        with open(file_path, 'rb') as file:
            return np.load(file)
    except Exception as e:
        raise CustomException(e, sys) from e