import sys
import os
import certifi
import dotenv
import pymongo
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from Network_security.pipelines.training_pipeline import TrainingPipeline
from Network_security.logger.logger import logging
from Network_security.Myexception.Myexception import CustomException
from Network_security.util.main_util.utils import load_object
from Network_security.constant.training_pipeline.consts import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DB_NAME,MODEL_TRAINER_TRAINED_MODEL_DIR,MODEL_TRAINER_TRAINED_MODEL_NAME
from fastapi.templating import Jinja2Templates
from Network_security.components.Network_model import Network_model
templates = Jinja2Templates(directory="./templates")
ca = certifi.where()
dotenv.load_dotenv(dotenv.find_dotenv())
url = os.getenv("MONGO_DB_URL")

client = pymongo.MongoClient(url, tlsCAFile=ca)
db = client[DATA_INGESTION_DB_NAME]
collection = db[DATA_INGESTION_COLLECTION_NAME]
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.initiate_training_pipeline()
        return ("Training pipeline initiated successfully")
    except Exception as e:
        raise CustomException(e, sys) from e
@app.post("/predict")
async def predict(request: Request, file: UploadFile = File(...)):
    try:
        print('entered')
        model_path = os.path.join("artifact","2025-07-08 19:22:07.978968",MODEL_TRAINER_TRAINED_MODEL_DIR, MODEL_TRAINER_TRAINED_MODEL_NAME)
        model:Network_model = load_object(model_path)
        df = pd.read_csv(file.file)
        X_pred = df.to_numpy()
        y_pred = model.predict(X_pred)
        df['prediction'] = y_pred
        os.makedirs("output", exist_ok=True)
        df.to_csv("output/predictions.csv", index=False)
        table_html = df.to_html(classes='table table-striped', index=False)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
        print(e)
        raise CustomException(e, sys) from e
if __name__ == "__main__":
    try:
        logging.info("Starting FastAPI application")
        app_run(app, host="localhost", port=8000)
    except Exception as e:
        raise CustomException(e, sys) from e