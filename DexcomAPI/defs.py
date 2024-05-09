# defs.py
import os
import mysql.connector
import pydexcom

def get_dexcom_connection():
    """Establish and return a connection to Dexcom using environment variables."""
    dexcom_username = os.getenv("DEXCOM_USERNAME")
    dexcom_password = os.getenv("DEXCOM_PASSWORD")
    return pydexcom.Dexcom(dexcom_username, dexcom_password)

def get_database_connection():
    """Connect to the SQL database using environment variables and return the connection."""
    return mysql.connector.connect(
        host=os.getenv("sql_host"),
        user=os.getenv("sql_user"),
        password=os.getenv("sql_password"),
        database=os.getenv("sql_database")
    )