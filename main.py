import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Define global variables for the loaded components
MODEL = None
IMPUTER = None
SCALER = None

try:
    MODEL = joblib.load('hybrid_diab_rf_ann_model.joblib')
    IMPUTER = joblib.load('imputer.joblib')
    SCALER = joblib.load('scaler.joblib')
    print("Model and preprocessors loaded successfully.")
except FileNotFoundError:
    print("ERROR: One or more joblib files are missing. Ensure all .joblib files are in the same directory.")
    pass 


IMPUTE_INDICES = [4, 5, 6]
SCALE_INDICES = [1, 4, 5, 6]
FEATURE_COLUMNS = [
    'gender', 'age', 'hypertension', 'heart_disease', 'bmi',
    'HbA1c_level', 'blood_glucose_level', 'smoking_history_numeric'
]

def preprocess_input(data_array: np.ndarray) -> np.ndarray:
    """Applies the same imputation and scaling steps as training."""
    
    X_imputed = data_array.copy()
    X_to_impute = X_imputed[:, IMPUTE_INDICES]
    X_imputed[:, IMPUTE_INDICES] = IMPUTER.transform(X_to_impute)
    
    X_scaled = X_imputed.copy()
    X_to_scale = X_scaled[:, SCALE_INDICES]
    X_scaled[:, SCALE_INDICES] = SCALER.transform(X_to_scale)
    
    return X_scaled


class PatientData(BaseModel):
    """Defines the structure and validation for the incoming JSON data."""
    gender: float = Field(..., ge=0, description="Gender (e.g., 0 or 1)")
    age: float = Field(..., gt=0, description="Age in years")
    hypertension: float = Field(..., ge=0, le=1, description="Hypertension status (0 or 1)")
    heart_disease: float = Field(..., ge=0, le=1, description="Heart disease status (0 or 1)")
    bmi: float = Field(..., gt=0, description="Body Mass Index")
    HbA1c_level: float = Field(..., gt=0, description="HbA1c level")
    blood_glucose_level: float = Field(..., gt=0, description="Blood glucose level")
    smoking_history_numeric: float = Field(..., ge=0, description="Smoking history (Encoded numerically)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "gender": 0.0,
                    "age": 45.0,
                    "hypertension": 0.0,
                    "heart_disease": 0.0,
                    "bmi": 28.5,
                    "HbA1c_level": 5.7,
                    "blood_glucose_level": 120.0,
                    "smoking_history_numeric": 1.0
                }
            ]
        }
    }

app = FastAPI(
    title="Diabetes Prediction API",
    description="A FastAPI service for predicting diabetes using a Hybrid RF-ANN Ensemble Model.",
    version="1.0.0",
)

@app.get("/")
def read_root():
    """Root endpoint for a simple health check."""
    return {"message": "Diabetes Prediction API is running. Go to /predict to use the model."}

@app.post("/predict")
async def predict_diabetes(data: PatientData):
    """
    Endpoint to receive patient data and return a diabetes prediction.
    
    The input data is automatically validated by the PatientData Pydantic model.
    """
    
    if MODEL is None or IMPUTER is None or SCALER is None:
        raise HTTPException(
            status_code=503,
            detail="Model components not loaded. Check server logs for FileNotFoundError.",
        )

    try:
        feature_values = [
            data.gender, data.age, data.hypertension, data.heart_disease, 
            data.bmi, data.HbA1c_level, data.blood_glucose_level, 
            data.smoking_history_numeric
        ]
        
        input_array = np.array(feature_values, dtype=float).reshape(1, -1)
        
        processed_data = preprocess_input(input_array)
        
        prediction_result = MODEL.predict(processed_data)[0] 
        
        result = {
            "prediction": int(prediction_result), # 0 or 1
            "diagnosis": "Diabetic" if prediction_result == 1 else "Non-Diabetic",
            "message": "Prediction made successfully by the Hybrid Diab-RF-ANN ensemble model."
        }
        
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during prediction: {str(e)}")