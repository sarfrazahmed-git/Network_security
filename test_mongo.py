from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from Network_security.logger.logger import logging
from Network_security.Myexception.Myexception import CustomException
import dotenv
import os
dotenv.load_dotenv(dotenv.find_dotenv())
uri = os.getenv("MONGO_DB_URL")
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    logging.info("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    logging.error(e)