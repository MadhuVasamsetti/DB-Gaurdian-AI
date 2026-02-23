# src/models/train_dummy_models.py
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib
from src.config import settings

# 1️⃣ Generate dummy dataset
np.random.seed(42)
X = np.random.rand(1000, 3) * 100  # CPU, RAM, Disk usage %
y = np.random.randint(0, 2, 1000)  # 0 = normal, 1 = anomaly

# Save dataset (optional)
df = pd.DataFrame(X, columns=['cpu','ram','disk'])
df['anomaly'] = y
df.to_csv(settings.DATASET_PATH, index=False)

# 2️⃣ Scale data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, settings.SCALER_PATH)

# 3️⃣ Train Random Forest
rf_model = RandomForestClassifier(n_estimators=100)
rf_model.fit(X_scaled, y)
joblib.dump(rf_model, settings.RF_MODEL_PATH)
print("✅ Random Forest model saved.")

# 4️⃣ Train simple LSTM
X_lstm = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))
lstm_model = Sequential()
lstm_model.add(LSTM(16, input_shape=(1,3), activation='relu'))
lstm_model.add(Dense(1, activation='sigmoid'))
lstm_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
lstm_model.fit(X_lstm, y, epochs=5, batch_size=16, verbose=1)
lstm_model.save(settings.LSTM_MODEL_PATH)
print("✅ LSTM model saved.")