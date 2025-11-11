from fastapi import FastAPI
from app.routes import auth_routes, predict_routes

app = FastAPI(
    title="Diabetes Prediction API",
    version="2.0.0",
    description="FastAPI + Brevo + Redis + ML Integration"
)

app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(predict_routes.router, prefix="/api", tags=["Prediction"])

@app.get("/")
def root():
    return {"message": " Diabetes Prediction API is running successfully."}
