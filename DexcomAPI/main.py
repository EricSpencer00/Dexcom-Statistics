# main.py
# MGDL Numbers

import os
import smtplib
import smtplib
import time
from datetime import datetime, timedelta
from pydexcom import Dexcom
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from defs import get_dexcom_env_variables, get_sender_email_credentials, get_receiver_email, get_database_connection
from stat_functions import verbose_message_mgdl, verbose_message_mmol, concise_message_mdgl, concise_message_mmol
from database import insert_glucose_readings, get_latest_notification, get_latest_timestamp
from stat_functions import get_current_value_mdgl, get_current_value_mmol
from collections import defaultdict

dexcom = get_dexcom_env_variables()
email_username, email_password = get_sender_email_credentials()
receiver_email = get_receiver_email()
db = get_database_connection()
db_name = os.getenv("sql_database")

# Print the data to console
# print("\n\nmg/dL data:\n")
# print(verbose_message_mgdl(dexcom))
# print("\n\nmmol/L data:\n")
# print(verbose_message_mmol(dexcom))
# print("\n\nmg/dL text message:\n")
# print(concise_message_mdgl(dexcom))
# print("\n\nmmol/L text message:\n")
# print(concise_message_mmol(dexcom))
# print("\n")

glucose_number = get_current_value_mdgl(dexcom)
glucose_time = dexcom.get_current_glucose_reading().datetime

def send_notification(email_username, email_password, receiver_email, dexcom):
    latest_notification, latest_timestamps = get_latest_notification(db, db_name)
    current_time = datetime.now()
    thirty_minutes_ago = current_time - timedelta(minutes=30)

    if latest_notification != 1 and current_time >= thirty_minutes_ago:
        message = MIMEMultipart()
        message["From"] = email_username
        message["To"] = receiver_email
        message.attach(MIMEText(concise_message_mdgl(dexcom), 'plain'))
        try:
            domain = email_username.split('@')[-1] # Support all email domains
            smtp_server = f"smtp.{domain}"
            smtp_port = 587
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_username, email_password)
                server.sendmail(email_username, receiver_email, message.as_string())
            print(f"Message sent successfully!")

            # Execute the update query
            cursor = db.cursor()
            latest_timestamp = get_latest_timestamp(cursor, db_name)
            if latest_timestamp:
                cursor.execute(f"UPDATE {db_name} SET notification = 1 WHERE timestamp = %s", (latest_timestamp,))
                db.commit()
                print("Notification flag updated successfully.")
            else:
                print("No timestamp found to update notification flag.")
            cursor.close()

        except Exception as e:
            print(f"error: {e}")
    else:
        print("No notification sent.")

if glucose_number <= 55 or glucose_number >= 180:
# if True:
    send_notification(email_username, email_password, receiver_email, dexcom)

try:
    insert_glucose_readings(dexcom, db, db_name)
finally:
    db.close()