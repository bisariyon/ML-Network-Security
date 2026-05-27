import sys
import os

import certifi

from src.constants.training_pipeline_constants import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME
from src.utils.main_utils import load_object
from src.utils.ml_model_utils import PredictionModel
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URI")
print(mongo_db_url)

import pymongo
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

from fastapi.responses import FileResponse
from fastapi import Body

FEATURE_COLUMNS = [
    'having_IP_Address', 'URL_Length', 'Shortining_Service', 'having_At_Symbol',
    'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State',
    'Domain_registeration_length', 'Favicon', 'port', 'HTTPS_token', 'Request_URL',
    'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Submitting_to_email', 'Abnormal_URL',
    'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain',
    'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page',
    'Statistical_report'
]

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/download_sample")
async def download_sample():
    file_path = "templates/sample_prediction_data.csv"
    return FileResponse(file_path, media_type="text/csv", filename="sample_prediction_data.csv")

@app.get("/download_predictions")
async def download_predictions():
    file_path = "prediction_output/output.csv"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/csv", filename="predictions.csv")
    return Response("No predictions found. Please run a prediction first.", status_code=404)

@app.post("/predict_single")
async def predict_single(data: dict = Body(...)):
    try:
        # Build the DataFrame in exact preprocessor fit order from FEATURE_COLUMNS
        # This guarantees no key mismatch or column ordering issues
        row = {col: int(data.get(col, 0)) for col in FEATURE_COLUMNS}
        df = pd.DataFrame([row], columns=FEATURE_COLUMNS)
            
        # preprocessor = load_object("final_model/preprocessor.pkl")
        # final_model = load_object("final_model/best_model.pkl")
        # network_model = PredictionModel(preprocessor=preprocessor, model=final_model)
        
        network_model = load_object("final_model/PredictionModel.pkl")
        
        y_pred = network_model.predict(df)
        prediction = int(y_pred[0])
        return {"prediction": prediction, "status": "Legitimate" if prediction == 1 else "Phishing"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

# @app.get("/train")
# async def train_route():
#     try:
#         train_pipeline=TrainingPipeline()
#         train_pipeline.run_pipeline()
#         return Response("Training is successful")
#     except Exception as e:
#         raise NetworkSecurityException(e,sys)
    
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        
        df_features = df.reindex(columns=FEATURE_COLUMNS)

        # preprocesor=load_object("final_model/preprocessor.pkl")
        # final_model=load_object("final_model/best_model.pkl")
        # network_model = PredictionModel(preprocessor=preprocesor,model=final_model)
        network_model = load_object("final_model/PredictionModel.pkl")


        y_pred = network_model.predict(df_features)
        
        # Insert Predicted_Result at the first column (index 0) so the user doesn't have to scroll right
        df.insert(0, 'Predicted_Result', y_pred)
        
        # If the original Result is present, move it next to the prediction (index 1)
        if 'Result' in df.columns:
            col_result = df.pop('Result')
            df.insert(1, 'Result', col_result)
        
        # Ensure directory for outputs exists
        os.makedirs('prediction_output', exist_ok=True)
        df.to_csv('prediction_output/output.csv', index=False)
        
        table_html = df.to_html(classes='table table-striped table-hover', index=False)

        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)

    
if __name__=="__main__":
    app_run(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
