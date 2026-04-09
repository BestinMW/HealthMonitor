import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# =========================
# 1. LOAD DATA
# =========================
df = pd.read_csv("vitals_dataset.csv")

# =========================
# 2. USE ONLY REQUIRED FEATURES
# =========================
features = [
    "Heart Rate (bpm)",
    "SpO2 Level (%)",
    "Body Temperature (°C)"
]

df = df[features].dropna()

# =========================
# 3. CREATE ABNORMALITY LABELS
# =========================
def label_abnormal(row):
    hr = row["Heart Rate (bpm)"]
    spo2 = row["SpO2 Level (%)"]
    temp = row["Body Temperature (°C)"]
    
    abnormalities = []
    
    # Heart Rate
    if hr < 60:
        abnormalities.append("Heart Rate Too Low")
    elif hr > 100:
        abnormalities.append("Heart Rate Too High")
    
    # SpO2
    if spo2 < 95:
        abnormalities.append("SpO2 Too Low")
    
    # Temperature
    if temp < 35:
        abnormalities.append("Temperature Too Low")
    elif temp >= 38:
        abnormalities.append("Temperature Too High")
    
    if len(abnormalities) == 0:
        return "Normal"
    
    return " | ".join(abnormalities)

df["Abnormality"] = df.apply(label_abnormal, axis=1)

# =========================
# 4. ENCODE LABELS
# =========================
X = df[features]
y = df["Abnormality"]

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# =========================
# 5. TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# =========================
# 6. TRAIN MODEL
# =========================
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# =========================
# 7. EVALUATE
# =========================
y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))

# =========================
# 8. SAVE MODEL
# =========================
joblib.dump(model, "abnormality_model.pkl")
joblib.dump(encoder, "abnormality_encoder.pkl")

print("Model saved successfully.")