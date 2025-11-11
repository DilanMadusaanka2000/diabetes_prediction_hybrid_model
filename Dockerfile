# Use a lightweight Python base image for a smaller final image size
FROM python:3.11-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

COPY main.py .
COPY hybrid_diab_rf_ann_model.joblib .
COPY imputer.joblib .
COPY scaler.joblib .

EXPOSE 80

# Command to run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]