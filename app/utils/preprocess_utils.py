import numpy as np
from app.utils.model_loader import IMPUTER, SCALER

IMPUTE_INDICES = [4, 5, 6]
SCALE_INDICES = [1, 4, 5, 6]

def preprocess_input(data_array: np.ndarray) -> np.ndarray:
    X_imputed = data_array.copy()
    X_to_impute = X_imputed[:, IMPUTE_INDICES]
    X_imputed[:, IMPUTE_INDICES] = IMPUTER.transform(X_to_impute)

    X_scaled = X_imputed.copy()
    X_to_scale = X_scaled[:, SCALE_INDICES]
    X_scaled[:, SCALE_INDICES] = SCALER.transform(X_to_scale)

    return X_scaled
