import os
import smtplib
import statistics
import matplotlib.pyplot as plt
from pydexcom import Dexcom
from typing import List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import smtplib

# Get the username and password from environment variables
dexcom_username = os.getenv("DEXCOM_USERNAME")
dexcom_password = os.getenv("DEXCOM_PASSWORD")
email_username = os.getenv("email_username")
email_password = os.getenv("email_password")
receiver_number = os.getenv("receiver_number")

smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Check accounts
if not dexcom_username:
    print("Error: DEXCOM_USERNAME environment variable is not set.")
    exit(1)
if not dexcom_password:
    print("Error: DEXCOM_PASSWORD environment variable is not set.")
    exit(1)
if not email_username:
    print("Error: email_username environment variable is not set.")
    exit(1)
if not email_password:
    print("Error: email_password environment variable is not set.")
    exit(1)
if not receiver_number:
    print("Error: receiver number environment variable is not set.")


dexcom = Dexcom(dexcom_username, dexcom_password) 

# Get current glucose reading
glucose_reading = dexcom.get_current_glucose_reading()
glucose_value = glucose_reading.value
trend_arrow = glucose_reading.trend_arrow

# Categorize glucose levels based on criteria
glucose_state = "Low" if glucose_value < 70 else "High" if glucose_value > 150 else "In Range"

# Create the graph data from past day's data
glucose_graph: List = dexcom.get_glucose_readings(minutes=1440, max_count=288)
glucose_values = [reading.value for reading in glucose_graph]
timestamps = [reading.datetime for reading in glucose_graph]
trend_arrows = [reading.trend_arrow for reading in glucose_graph]

# Create the graph plt
plt.figure(figsize=(10, 5))
plt.plot(timestamps, glucose_values, color='black', linewidth=1)

# Highlight low, in-range, and high glucose levels
low_glucose = [idx for idx, reading in enumerate(glucose_values) if reading < 70]
in_range_glucose = [idx for idx, reading in enumerate(glucose_values) if 70 <= reading <= 150]
high_glucose = [idx for idx, reading in enumerate(glucose_values) if reading > 150]

if low_glucose:
    plt.axhline(y=min(glucose_values), color='red', linestyle='--', linewidth=1, alpha=0.5, xmin=min(low_glucose)/len(glucose_values), xmax=max(low_glucose)/len(glucose_values)) # Low glucose
if high_glucose:
    plt.axhline(y=max(glucose_values), color='red', linestyle='--', linewidth=1, alpha=0.5, xmin=min(high_glucose)/len(glucose_values), xmax=max(high_glucose)/len(glucose_values)) # High glucose
if in_range_glucose:
    plt.axhline(y=70, color='green', linestyle='--', linewidth=1, alpha=0.5, xmin=min(in_range_glucose)/len(glucose_values), xmax=max(in_range_glucose)/len(glucose_values)) # In-range glucose
    plt.axhline(y=150, color='green', linestyle='--', linewidth=1, alpha=0.5, xmin=min(in_range_glucose)/len(glucose_values), xmax=max(in_range_glucose)/len(glucose_values)) # In-range glucose

# Plot trend arrows
for i, arrow in enumerate(trend_arrows):
    if arrow == "↑":
        plt.scatter(timestamps[i], glucose_values[i], color='green', marker='^', s=50)
    elif arrow == "↓":
        plt.scatter(timestamps[i], glucose_values[i], color='red', marker='v', s=50)
    else:
        plt.scatter(timestamps[i], glucose_values[i], color='orange', marker='o', s=50)

# Plot settings
plt.title('Dexcom Glucose Readings Over the Past Day')
plt.xlabel('Time (Day / Hour)')
plt.ylabel('Glucose Level (mg/dL)')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot as an image
plt.savefig('dexcom_glucose_graph.png')

# Calculate glucose statistics
average_glucose_mgdl = round(statistics.mean(glucose_values), 4)
median_glucose_mgdl = round(statistics.median(glucose_values), 4)
stdev_glucose_mgdl = round(statistics.stdev(glucose_values), 4)
min_glucose_mgdl = min(glucose_values)
max_glucose_mgdl = max(glucose_values)
glucose_range_mgdl = max_glucose_mgdl - min_glucose_mgdl

# Calculate Time in Range
time_in_range_percentage = round((len(in_range_glucose) / len(glucose_values)) * 100, 4)

# Calculate Glycemic Variability Index
mgdl_above_180 = sum(reading - 180 for reading in glucose_values if reading > 180)
mgdl_below_70 = sum(70 - reading for reading in glucose_values if reading < 70)
total_area = (max_glucose_mgdl - 180) * time_in_range_percentage / 100 + mgdl_above_180 + mgdl_below_70
glycemic_variability_index = ((mgdl_above_180 + mgdl_below_70) / total_area) * 100

# Use ADAG formula to estimate A1C
average_glucose_mmol = round(average_glucose_mgdl / 18.01559, 4)
estimated_a1c = round((28.7 * average_glucose_mmol + 46.7) / 28.7, 4)

# Create message
message_body = f"Your current glucose level is {glucose_value} mg/dL ({glucose_reading.trend_description} {trend_arrow})\n" \
               f"Time of reading: {glucose_reading.datetime}\n" \
               f"Glucose state: {glucose_state}\n" \
               f"Average glucose level: {average_glucose_mgdl} mg/dL\n" \
               f"Estimated A1C: {estimated_a1c}\n" \
               f"Time in Range (70-150 mg/dL): {time_in_range_percentage:.2f}%\n" \
               f"Median Glucose: {median_glucose_mgdl} mg/dL\n" \
               f"Standard Deviation: {stdev_glucose_mgdl} mg/dL\n" \
               f"Minimum Glucose: {min_glucose_mgdl} mg/dL\n" \
               f"Maximum Glucose: {max_glucose_mgdl} mg/dL\n" \
               f"Glucose Range: {glucose_range_mgdl} mg/dL\n" \
               f"Coef. of Variation: {round((stdev_glucose_mgdl / average_glucose_mgdl) * 100, 4)}%\n" \
               f"Glycemic Variability Index: {glycemic_variability_index}%"

message_concise = f"{glucose_value} and {glucose_reading.trend_description}"

# Print the data to console
print(message_body)
print(message_concise)

message = MIMEMultipart()
message["From"] = email_username
message["To"] = receiver_number

message.attach(MIMEText(message_concise, 'plain'))

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_username, email_password)
        server.sendmail(email_username, receiver_number, message.as_string())
    print("success!")
except Exception as e:
    print(f"error: {e}")

# Display graph
# plt.show()

