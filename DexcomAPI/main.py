import os
import statistics
import matplotlib.pyplot as plt
from pydexcom import Dexcom
from asciichartpy import plot
from typing import List

# Categorize glucose levels based on criteria
def categorize_glucose(glucose_value, trend_arrow):
    """
    Categorize glucose levels based on the provided criteria.
    
    Args:
        glucose_value (float): Glucose value.
        trend_arrow (str): Trend arrow direction ("<", ">", or "-").
    
    Returns:
        str: Categorized state of glucose level.
    """
    # Glucose level categorization based on provided criteria
    if glucose_value < 80 and trend_arrow == "↓":
        return "Low"
    elif glucose_value < 70:
        return "Low"
    elif 80 <= glucose_value < 140 and trend_arrow != "↑":
        return "In Range"
    elif glucose_value < 150 and trend_arrow != "↑":
        return "In Range"
    elif glucose_value > 140 and trend_arrow == "↑":
        return "High"
    elif glucose_value > 150:
        return "High"
    else:
        return "Unknown"

# Get the username and password from environment variables
username = os.getenv("DEXCOM_USERNAME")
password = os.getenv("DEXCOM_PASSWORD")

# Check
if not username or not password:
    print("Error: DEXCOM_USERNAME or DEXCOM_PASSWORD environment variables are not set.")
    exit(1)

dexcom = Dexcom(username, password)   

# Get current glucose reading
glucose_reading = dexcom.get_current_glucose_reading()
glucose_value = glucose_reading.value
trend_arrow = glucose_reading.trend_arrow

# Categorize the glucose level
glucose_state = categorize_glucose(glucose_value, trend_arrow)

# Create the graph data from past day's data
glucose_graph: List = dexcom.get_glucose_readings(minutes=1440, max_count=288)
glucose_values = [reading.value for reading in glucose_graph]
timestamps = [reading.datetime for reading in glucose_graph]

# Create the graph plt
plt.figure(figsize=(10, 5))
plt.plot(timestamps, glucose_values, marker='o', linestyle='-')
plt.title('Glucose Readings Over the Past Day')
plt.xlabel('Time')
plt.ylabel('Glucose Level (mg/dL)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Create the ascii chart
height = 180

# Calculate the average, mean, median, etc glucose value
total_glucose_mgdl = sum(glucose_values)
average_glucose_mgdl = round(total_glucose_mgdl / len(glucose_values), 4)
mean_glucose_mgdl = round(statistics.mean(glucose_values), 4)
median_glucose_mgdl = round(statistics.median(glucose_values), 4)
stdev_glucose_mgdl = round(statistics.stdev(glucose_values), 4)
variance_glucose_mgdl = round(statistics.variance(glucose_values), 4)
min_glucose_mgdl = min(glucose_values)
max_glucose_mgdl = max(glucose_values)
glucose_range_mgdl = max_glucose_mgdl - min_glucose_mgdl

q1 = statistics.quantiles(glucose_values, n=4)[0]
q3 = statistics.quantiles(glucose_values, n=4)[-1]
iqr = q3 - q1

coeff_var_glucose_mgdl = round((stdev_glucose_mgdl / average_glucose_mgdl) * 100, 4)

# Calculate Time in Range
time_in_range = 0
for reading in glucose_values:
    if 70 <= reading <= 150:
        time_in_range += 1
total_time = len(glucose_values)
time_in_range_percentage = round((time_in_range / total_time) * 100, 4)

# Use ADAG formula to estimate A1C
average_glucose_mmol = round(average_glucose_mgdl / 18.01559, 4)
estimated_a1c = round((28.7 * average_glucose_mmol + 46.7) / 28.7, 4)

# Print the data

print(f"Your current glucose level is {glucose_value} mg/dL ({glucose_reading.trend_description} {trend_arrow})")
print(f"Time of reading: {glucose_reading.datetime}")
print(f"Glucose state: {glucose_state}")
print(f"Average glucose level: {average_glucose_mgdl} mg/dL")
print(f"Estimated A1C: {estimated_a1c}")
print(f"Time in Range (70-150 mg/dL): {time_in_range_percentage:.2f}%")


# Display MatLab graph
plt.show()
