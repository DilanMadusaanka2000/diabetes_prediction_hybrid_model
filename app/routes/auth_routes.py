from fastapi import APIRouter, HTTPException
from app.models.patient_model import LoginInitRequest, VerifyOtpRequest
from app.services.otp_service import generate_otp, generate_token, store_otp
from app.config.settings import redis_client
from app.config.brevo_config import send_otp_email

router = APIRouter()

@router.post("/login/init")
def login_init(request: LoginInitRequest):
    username = request.username.lower()
    otp = generate_otp()
    token = generate_token()
    store_otp(username, otp, token)

    if not send_otp_email(username, otp):
        raise HTTPException(status_code=500, detail="Failed to send OTP email.")

    return {"message": "OTP sent to your email.", "token": token}

@router.post("/login/verify")
def verify_otp(request: VerifyOtpRequest):
    redis_key = f"user:{request.username.lower()}"
    stored_data = redis_client.hgetall(redis_key)

    if not stored_data:
        raise HTTPException(status_code=400, detail="OTP expired or user not found.")
    if stored_data.get("token") != request.token:
        raise HTTPException(status_code=400, detail="Invalid token.")
    if stored_data.get("otp") != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP.")

    redis_client.delete(redis_key)
    return {"message": "OTP verified successfully!", "status": "success"}
