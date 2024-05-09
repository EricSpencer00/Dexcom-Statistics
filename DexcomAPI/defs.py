# defs.py
import os
import mysql.connector
import pydexcom
from twilio.rest import Client

def get_dexcom_connection():
    """Establish and return a connection to Dexcom using environment variables"""
    dexcom_username = os.getenv("dexcom_username")
    dexcom_password = os.getenv("dexcom_password")
    return pydexcom.Dexcom(dexcom_username, dexcom_password)

def get_database_connection():
    """Connect to the SQL database using environment variables and return the connection"""
    return mysql.connector.connect(
        host=os.getenv("sql_host"),
        user=os.getenv("sql_user"),
        password=os.getenv("sql_password"),
        database=os.getenv("sql_database")
    )

def get_sender_email_credentials():
    """Retrieve sender's email credentials from environment variables"""
    email_username = os.getenv("email_username")
    email_password = os.getenv("email_password")
    return email_username, email_password

def get_receiver_email():
    """Retrieve receiver's email from environment variables"""
    receiver_email = os.getenv("receiver_email")
    return receiver_email

def get_twilio_client():
    """Return Twilio client using environment variables"""
    account_sid = os.getenv("twilio_account_sid")
    auth_token = os.getenv("twilio_auth_token")
    twilio_from = os.getenv("twilio_from")
    twilio_to = os.getenv("twilio_to")
    return Client(account_sid, auth_token, twilio_from, twilio_to)