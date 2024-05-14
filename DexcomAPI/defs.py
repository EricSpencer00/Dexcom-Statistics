# defs.py
import os
import mysql.connector
import pydexcom
from dotenv import load_dotenv
from twilio.rest import Client
from authlib.integrations.flask_client import OAuth
import requests

load_dotenv()

def get_dexcom_connection():
    """Establish and return a connection to Dexcom using environment variables"""
    dexcom_username = os.getenv("dexcom_username")
    dexcom_password = os.getenv("dexcom_password")

    if not dexcom_username or not dexcom_password:
        raise ValueError("Dexcom username and password must be set as environment variables.")

    return pydexcom.Dexcom(dexcom_username, dexcom_password)

def get_dexcom_connection_access():
    """Establish and return a connection to Dexcom using AuthLib OAuth request"""
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    access_token = get_access_token(client_id, client_secret)
    """ Don't return pydexcom object, not required here as we make
    call to Dexcom themselves """
    # return pydexcom.Dexcom(access_token=access_token)
    return 0

def get_access_token(client_id, client_secret):
    token_url = "https://api.dexcom.com/v2/oauth2/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Failed to obtain access token")

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