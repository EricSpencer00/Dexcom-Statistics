import os
from pydexcom import Dexcom

# Check if Dexcom credentials are provided as environment variables
username = os.environ.get("DEXCOM_USERNAME")
password = os.environ.get("DEXCOM_PASSWORD")

if username is None or password is None:
    print("Please set DEXCOM_USERNAME and DEXCOM_PASSWORD environment variables.")
    exit(1)

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
        return "Good / Neutral"
    elif glucose_value < 150 and trend_arrow != "↑":
        return "Good / Neutral"
    elif glucose_value > 140 and trend_arrow == "↑":
        return "High"
    elif glucose_value > 150:
        return "High"
    else:
        return "Unknown"

# Initialize Dexcom API
dexcom = Dexcom(username, password)

# Get current glucose reading
glucose_reading = dexcom.get_current_glucose_reading()
minutes: int
#glucose_graph = dexcom.get_glucose_readings(minutes: int = 1440, max_count: int = 288) -> List[glucose_graph]:
glucose_value = glucose_reading.value
trend_arrow = glucose_reading.trend_arrow

# Categorize the glucose level
glucose_state = categorize_glucose(glucose_value, trend_arrow)

# Print the categorized state
print(f"Your current glucose level is {glucose_value} mg/dL ({glucose_reading.trend_description} {trend_arrow})")
print(f"Time of reading: {glucose_reading.datetime}")
print(f"Glucose state: {glucose_state}")

