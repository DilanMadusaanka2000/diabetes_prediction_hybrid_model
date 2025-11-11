import string
import uuid
import random
from app.config.settings import redis_client

OTP_EXPIRATION = 300  # seconds

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def generate_token():
    return str(uuid.uuid4())

def store_otp(username: str, otp: str, token: str):
    redis_key = f"user:{username}"
    redis_client.hset(redis_key, mapping={"otp": otp, "token": token})
    redis_client.expire(redis_key, OTP_EXPIRATION)
