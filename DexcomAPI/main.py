# MGDL numbers

import os
import smtplib
import statistics
from pydexcom import Dexcom
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from defs import get_dexcom_connection, get_sender_email_credentials, get_receiver_email, get_database_connection
from stat_functions import verbose_message_mgdl, verbose_message_mmol, concise_message_mdgl, concise_message_mmol
from database import insert_glucose_readings

# Initialize variables
dexcom = get_dexcom_connection()
email_username, email_password = get_sender_email_credentials()
receiver_email = get_receiver_email()

# Print the data to console
print(verbose_message_mgdl(dexcom))
print(verbose_message_mmol(dexcom))
print(concise_message_mdgl(dexcom))
print(concise_message_mmol(dexcom))

message = MIMEMultipart()
message["From"] = email_username
message["To"] = receiver_email
message["Subject"] = "Glucose Level Alert"

# Output to phone number
message.attach(MIMEText(concise_message_mdgl(dexcom), 'plain'))

# try:
#     domain = email_username.split('@')[-1] # Support all email domains
#     smtp_server = f"smtp.{domain}"
#     smtp_port = 587
#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()
#         server.login(email_username, email_password)
#         server.sendmail(email_username, receiver_email, message.as_string())
#     print("Message sent successfully")
# except Exception as e:
#     print(f"error: {e}")

# Insert past 24 hours into database
db = get_database_connection()
db_name = os.getenv("sql_database")

try: 
    insert_glucose_readings(dexcom, db, db_name)
finally:
    db.close()