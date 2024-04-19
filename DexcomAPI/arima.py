import os
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from pydexcom import Dexcom
from typing import Dict, Any

dexcom_username = os.getenv("DEXCOM_USERNAME")
dexcom_password = os.getenv("DEXCOM_PASSWORD")
dexcom = Dexcom(dexcom_username, dexcom_password) 

# Get glucose readings and put into dictionary
glucose_reading = dexcom.get_glucose_readings(minutes=1440, max_count=288)
glucose_values = [reading.value for reading in glucose_reading]
timestamps = [reading.datetime for reading in glucose_reading]
trends = [reading.trend_description for reading in glucose_reading]

glucose_data = {
    "timestamps": timestamps,
    "glucose_values": glucose_values,
    "trends": trends
}

print(glucose_data)