import joblib

# Load your existing model
input_path = "hybrid_diab_rf_ann_model.joblib"
output_path = "hybrid_diab_rf_ann_model_v2.joblib"

print("Loading old model...")
model = joblib.load(input_path)

print("Saving converted model...")
joblib.dump(model, output_path)

print(f"✅ Model successfully saved as: {output_path}")
