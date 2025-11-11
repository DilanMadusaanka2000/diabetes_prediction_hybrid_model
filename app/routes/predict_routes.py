from fastapi import APIRouter, HTTPException
from app.models.patient_model import PatientData
from app.utils.model_loader import MODEL, IMPUTER, SCALER
from app.utils.preprocess_utils import preprocess_input
from app.services.genai_service import get_diabetes_resources
import numpy as np

router = APIRouter()

@router.post("/predict")
async def predict_diabetes(data: PatientData):
    if MODEL is None or IMPUTER is None or SCALER is None:
        raise HTTPException(status_code=503, detail="Model components not loaded.")

    try:
        # Validate input ranges
        if not (0 < data.age <= 120):
            raise HTTPException(status_code=400, detail="Invalid age value.")
        if not (10 <= data.bmi <= 60):
            raise HTTPException(status_code=400, detail="Invalid BMI value.")
        if not (3 <= data.HbA1c_level <= 15):
            raise HTTPException(status_code=400, detail="Invalid HbA1c value.")
        if not (50 <= data.blood_glucose_level <= 600):
            raise HTTPException(status_code=400, detail="Invalid blood glucose level.")

        # Preprocess
        values = [
            data.gender, data.age, data.hypertension, data.heart_disease,
            data.bmi, data.HbA1c_level, data.blood_glucose_level, data.smoking_history_numeric
        ]
        arr = np.array(values, dtype=float).reshape(1, -1)
        processed = preprocess_input(arr)
        pred = MODEL.predict(processed)[0]

        diagnosis = "Diabetic" if pred == 1 else "Non-Diabetic"
        ai_links = None

        # Only get AI links for diabetic patients
        if pred == 1:
            ai_links = get_diabetes_resources()

        return {
            "prediction": int(pred),
            "diagnosis": diagnosis,
            "ai_resources": ai_links
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
