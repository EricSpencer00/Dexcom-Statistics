'''
Slope prediction model, take 5 most recent points and predict next 3 values
Meant as a predictor of IOB or Glucose Rising trends as they are linear.
'''

import os
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from pydexcom import Dexcom

# Initialize Dexcom client
dexcom_username = os.getenv("DEXCOM_USERNAME")
dexcom_password = os.getenv("DEXCOM_PASSWORD")
dexcom = Dexcom(dexcom_username, dexcom_password)

# Get glucose readings and put into DataFrame
glucose_reading = dexcom.get_glucose_readings(minutes=1440, max_count=288)
glucose_values = [reading.value for reading in glucose_reading]
timestamps = [reading.datetime for reading in glucose_reading]

glucose_data = pd.DataFrame({
    "timestamps": timestamps,
    "glucose_values": glucose_values
})

current_time = datetime.datetime.now().strftime("%I:%M%p")
current_glucose = glucose_data.iloc[0]["glucose_values"]
print(f"Current Glucose Value at {current_time} (CDT): {current_glucose:.2f}")

# Select the 5 most recent points
glucose_data = glucose_data.sort_values(by="timestamps", ascending=False).head(5)

# Prepare data
X = glucose_data[["timestamps"]].astype(int) // 10**9
y = glucose_data["glucose_values"]

# Train the model
model = LinearRegression()
model.fit(X, y)

# Predict the next 3 values
last_timestamp = max(timestamps) if timestamps else datetime.datetime.now()
next_timestamps = [last_timestamp + datetime.timedelta(minutes=5) * (i+1) for i in range(4)]

next_predictions = pd.DataFrame({
    "timestamps": next_timestamps
})

next_predictions["timestamps"] = next_predictions["timestamps"].astype(int) // 10**9

# Predict the glucose values for the next timestamps
next_glucose_values = model.predict(next_predictions)
next_glucose_values = np.maximum(next_glucose_values, 0)

print(f"Current time: {datetime.datetime.now().strftime('%I:%M%p')} (CDT) - Trend: {next_glucose_values[0]:.2f}\n")
print("Predicting future glucose levels...")
for i in range(1, len(next_timestamps)):
    time_string = (datetime.datetime.now() + datetime.timedelta(minutes=5*i)).strftime('%I:%M%p')
    print(f"{time_string} (CDT) - Trend: {next_glucose_values[i]:.2f}")
