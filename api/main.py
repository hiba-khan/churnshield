import pickle
import json
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# load model
with open("data/best_model.pkl", "rb") as f:
    model = pickle.load(f)

# load expected columns
with open("data/model_columns.json", "r") as f:
    model_columns = json.load(f)

app = FastAPI(title="ChurnShield API", version="1.0")

class CustomerData(BaseModel):
    tenure: float
    MonthlyCharges: float
    TotalCharges: float
    SeniorCitizen: int
    Partner: int
    Dependents: int
    PhoneService: int
    PaperlessBilling: int
    charges_per_tenure: float
    senior_high_charges: int = 0
    gender_Male: int = 0
    MultipleLines_Yes: int = 0
    InternetService_Fiber_optic: int = 0
    InternetService_No: int = 0
    OnlineSecurity_Yes: int = 0
    OnlineBackup_Yes: int = 0
    DeviceProtection_Yes: int = 0
    TechSupport_Yes: int = 0
    StreamingTV_Yes: int = 0
    StreamingMovies_Yes: int = 0
    Contract_One_year: int = 0
    Contract_Two_year: int = 0
    PaymentMethod_Credit_card_automatic: int = 0
    PaymentMethod_Electronic_check: int = 0
    PaymentMethod_Mailed_check: int = 0
    tenure_group_mid: int = 0
    tenure_group_loyal: int = 0

@app.get("/")
def health_check():
    return {"status": "ok", "message": "ChurnShield API is running"}

@app.post("/predict")
def predict_churn(customer: CustomerData):
    # convert to dict and rename columns back to original
    input_dict = customer.dict()
    
    rename_map = {
        "InternetService_Fiber_optic": "InternetService_Fiber optic",
        "OnlineSecurity_Yes": "OnlineSecurity_Yes",
        "Contract_One_year": "Contract_One year",
        "Contract_Two_year": "Contract_Two year",
        "PaymentMethod_Credit_card_automatic": "PaymentMethod_Credit card (automatic)",
        "PaymentMethod_Electronic_check": "PaymentMethod_Electronic check",
        "PaymentMethod_Mailed_check": "PaymentMethod_Mailed check",
    }
    
    renamed = {rename_map.get(k, k): v for k, v in input_dict.items()}
    
    # create dataframe with all model columns, fill missing with 0
    df = pd.DataFrame([renamed])
    df = df.reindex(columns=model_columns, fill_value=0)
    
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    
    return {
        "churn_prediction": int(prediction),
        "churn_probability": round(float(probability), 3),
        "risk_level": "high" if probability > 0.7 else "medium" if probability > 0.4 else "low"
    }