# MGDL numbers

# import os
import time
import smtplib
from pydexcom import Dexcom
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from defs import get_dexcom_connection, get_sender_email_credentials, get_receiver_email, get_database_connection
from stat_functions import verbose_message_mgdl, verbose_message_mmol, concise_message_mdgl, concise_message_mmol
# from database import insert_glucose_readings
from stat_functions import get_current_value_mdgl, get_current_value_mmol

# Initialize variables
dexcom = get_dexcom_connection()
email_username, email_password = get_sender_email_credentials()
receiver_email = get_receiver_email()

last_notification = {}

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

if glucose_number <= 55 or glucose_number >= 180:
    if(time.time() - last_notification.get("time", 0) > 1800): # 30 minutes
        last_notification["time"] = time.time()
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
            print(f"Message sent successfully: {message}")
        except Exception as e:
            print(f"error: {e}")