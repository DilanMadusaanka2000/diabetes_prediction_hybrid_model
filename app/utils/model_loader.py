import joblib
import os

MODEL = None
IMPUTER = None
SCALER = None

def load_model_components():
    """Loads model, imputer, and scaler into memory."""
    global MODEL, IMPUTER, SCALER

    try:
        base_path = os.path.join(os.path.dirname(__file__), "../../models")
        MODEL = joblib.load(os.path.join(base_path, "hybrid_diab_rf_ann_model.joblib"))
        IMPUTER = joblib.load(os.path.join(base_path, "imputer.joblib"))
        SCALER = joblib.load(os.path.join(base_path, "scaler.joblib"))
        print(" Model and preprocessors loaded successfully.")
    except FileNotFoundError:
        print(" ERROR: Missing .joblib files in /models folder.")
        MODEL, IMPUTER, SCALER = None, None, None

load_model_components()
