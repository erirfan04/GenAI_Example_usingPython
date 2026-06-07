
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np

# 1️⃣ Create FastAPI app FIRST
app = FastAPI()

# 2️⃣ Load trained model
model = joblib.load("model.pkl")

# 3️⃣ Single prediction endpoint
class InputData(BaseModel):
    hours: float

@app.post("/predict")
def predict(data: InputData):
    X = np.array([[data.hours]])
    prediction = model.predict(X)
    return {"predicted_marks": float(prediction[0])}

# 4️⃣ CSV batch prediction endpoint
from io import BytesIO

@app.post("/predict_csv")
async def predict_csv(file: UploadFile = File(...)):

    contents = await file.read()
    buffer = BytesIO(contents)

    filename = file.filename.lower()

    if filename.endswith(".xlsx"):
        df = pd.read_excel(buffer)
    else:
        df = pd.read_csv(buffer, encoding="latin1")

    if "hours" not in df.columns:
        return {"error": "CSV must contain 'hours' column"}

    X = df[["hours"]].values
    predictions = model.predict(X)

    df["predicted_marks"] = predictions

    return df.to_dict(orient="records")


    # uvicorn main:app --reload 