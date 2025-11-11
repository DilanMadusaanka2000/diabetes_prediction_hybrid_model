from pydantic import BaseModel, Field

class PatientData(BaseModel):
    gender: float
    age: float
    hypertension: float
    heart_disease: float
    bmi: float
    HbA1c_level: float
    blood_glucose_level: float
    smoking_history_numeric: float

class LoginInitRequest(BaseModel):
    username: str

class VerifyOtpRequest(BaseModel):
    username: str
    otp: str
    token: str
