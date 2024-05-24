# defs.py
import os
import mysql.connector
import pydexcom
from dotenv import load_dotenv
from twilio.rest import Client
from authlib.integrations.flask_client import OAuth
import requests

load_dotenv()

def get_dexcom_env_variables():
    """Establish and return a connection to Dexcom using environment variables"""
    dexcom_username = os.getenv("dexcom_username")
    dexcom_password = os.getenv("dexcom_password")

    if not dexcom_username or not dexcom_password:
        raise ValueError("Dexcom username and password must be set as environment variables.")

    return pydexcom.Dexcom(dexcom_username, dexcom_password)

def get_dexcom_connection_access():
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    access_token = get_access_token(client_id, client_secret)
    # return pydexcom.Dexcom(access_token=access_token)
    # Replace with Dexcom Establish Connection ^^^
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
    return mysql.connector.connect(
        host=os.getenv("sql_host"),
        user=os.getenv("sql_user"),
        password=os.getenv("sql_password"),
        database=os.getenv("sql_database")
    )

def get_database_name():
    return os.getenv("sql_database")

def get_sender_email_credentials():
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

def get_sms_gateway(phone_number, carrier):
    gateways = {
        'AT&T': 'txt.att.net',
        'Verizon': 'vtext.com',
        'T-Mobile': 'tmomail.net',
        'Sprint': 'messaging.sprintpcs.com'
    }
    return f"{phone_number}@{gateways[carrier]}"

def get_oauth():
    oauth = OAuth()
    oauth.register(
        name='google',
        client_id=os.getenv("google_client_id"),
        client_secret=os.getenv("google_client_secret"),
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        refresh_token_url=None,
        refresh_token_params=None,
        scope='email',
        redirect_uri='http://localhost:5000/oauth/google'
    )
    return oauth

def get_oauth_token():
    return os.getenv("oauth_token")

def get_oauth_secret():
    return os.getenv("oauth_secret")

def get_oauth_provider():
    return os.getenv("oauth_provider")

def get_oauth_user():
    return os.getenv("oauth_user")

def get_oauth_user_id():
    return os.getenv("oauth_user_id")

def get_oauth_user_email():
    return os.getenv("oauth_user_email")

def get_oauth_user_name():
    return os.getenv("oauth_user_name")

def get_oauth_user_picture():
    return os.getenv("oauth_user_picture")

def get_oauth_user_locale():
    return os.getenv("oauth_user_locale")

def get_oauth_user_timezone():
    return os.getenv("oauth_user_timezone")