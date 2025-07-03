import os
import sys
import json

import dotenv
import certifi
import pandas as pd
import numpy as np
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from Network_security.logger.logger import logging
from Network_security.Myexception.Myexception import CustomException


dotenv.load_dotenv(dotenv.find_dotenv())
url = os.getenv("MONGO_DB_URL")

ca = certifi.where()
class NetworkDataextract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(f"Error in NetworkDataextract init: {e}", sys)
        
    def cv_to_json(self, file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            records = list(json.loads(df.to_json(orient="records")))
            return records
        except Exception as e:
            raise CustomException(e,sys)
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = MongoClient(url, server_api=ServerApi("1"))
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            CustomException(e,sys)



if __name__ == "__main__":
    File_path = "Network_data/phisingData.csv"
    DATABASE = "srfai"
    collection = "Networkdata"
    networkobj = NetworkDataextract()
    jsonobj = networkobj.cv_to_json(File_path)
    n_record = networkobj.insert_data_mongodb(jsonobj,DATABASE,collection)