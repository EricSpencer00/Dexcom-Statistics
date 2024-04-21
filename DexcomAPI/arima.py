import os
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from pydexcom import Dexcom

# Initialize Dexcom client
dexcom_username = os.getenv("DEXCOM_USERNAME")
dexcom_password = os.getenv("DEXCOM_PASSWORD")
dexcom = Dexcom(dexcom_username, dexcom_password)

# Get glucose readings and put into DataFrame
glucose_reading = dexcom.get_glucose_readings(minutes=1440, max_count=288)
glucose_values = [reading.value for reading in glucose_reading]
timestamps = [reading.datetime for reading in glucose_reading]
trends = [reading.trend_description for reading in glucose_reading]
trend_arrows = [reading.trend_arrow for reading in glucose_reading]

glucose_data = pd.DataFrame({
    "timestamps": timestamps,
    "glucose_values": glucose_values,
    "trends": trends,
    "trend_arrows": trend_arrows
})

# Split data into features (timestamps and trends) and target (glucose_values)
X = glucose_data[["timestamps", "trends"]]
y = glucose_data["glucose_values"]

# Converting timestamps to seconds since epoch for better model compatibility
X["timestamps"] = X["timestamps"].astype(int) // 10**9

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# One-hot encode the 'trends' column
encoder = OneHotEncoder()
trend_encoded = encoder.fit_transform(X_train[['trends']])
trend_encoded_test = encoder.transform(X_test[['trends']])

# Convert the encoded array into a DataFrame
trend_encoded_df = pd.DataFrame(trend_encoded.toarray(), columns=encoder.get_feature_names_out(['trends']))
trend_encoded_df_test = pd.DataFrame(trend_encoded_test.toarray(), columns=encoder.get_feature_names_out(['trends']))

# Drop the original 'trends' column and concatenate the encoded DataFrame
X_train_encoded = X_train.drop(columns=['trends']).reset_index(drop=True)
X_test_encoded = X_test.drop(columns=['trends']).reset_index(drop=True)

X_train_encoded = pd.concat([X_train_encoded, trend_encoded_df], axis=1)
X_test_encoded = pd.concat([X_test_encoded, trend_encoded_df_test], axis=1)

# Train the model
model = LinearRegression()
model.fit(X_train_encoded, y_train)

# Make predictions for the next 3 timestamps
next_timestamps = [max(timestamps) + (i + 1) * 60 for i in range(3)]  # Assuming timestamps are in seconds
next_trends = ["up", "down", "steady"]  # Assuming trend directions
next_timestamps_encoded = [[ts, trends == next_trends] for ts in next_timestamps]

# Convert to DataFrame and one-hot encode trend column
next_timestamps_df = pd.DataFrame(next_timestamps_encoded, columns=["timestamps", "trends"])
next_timestamps_df["timestamps"] = next_timestamps_df["timestamps"].astype(int) // 10**9
next_trends_encoded = encoder.transform(next_timestamps_df[['trends']])
next_trends_encoded_df = pd.DataFrame(next_trends_encoded.toarray(), columns=encoder.get_feature_names_out(['trends']))
next_timestamps_df_encoded = pd.concat([next_timestamps_df.drop(columns=['trends']), next_trends_encoded_df], axis=1)

# Predict glucose values for the next 3 timestamps
next_glucose_values = model.predict(next_timestamps_df_encoded)
print("Predicted Glucose Values for the Next 3 Timestamps:", next_glucose_values)
