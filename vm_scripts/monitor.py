import joblib
import numpy as np

# Load model
model = joblib.load("abnormality_model.pkl")
encoder = joblib.load("abnormality_encoder.pkl")

def check_vitals(hr, spo2, temp):
    
    input_data = np.array([[hr, spo2, temp]])
    prediction = model.predict(input_data)
    result = encoder.inverse_transform(prediction)[0]
    
    print("\n--- Vital Analysis ---")
    print(f"Heart Rate: {hr} bpm")
    print(f"SpO2: {spo2}%")
    print(f"Temperature: {temp}°C")
    
    if result == "Normal":
        print("Status: All vitals within normal range.")
    else:
        print("Status: Abnormalities detected:")
        print(result)
        print("Recommendation: Consider medical evaluation if symptoms persist.")
    
    print("-----------------------\n")


# Example test
check_vitals(110, 93, 38.5)