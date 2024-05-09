import datetime
import pydexcom
import mysql.connector
import os

db_connection = mysql.connector.connect(
    host = os.genenv("sql_host"),
    user = os.getenv("sql_user"),
    password = os.getenv("sql_password"),
    database = os.getenv("sql_database")
)
cursor = db_connection.cursor()

dexcom_username = os.getenv("DEXCOM_USERNAME")
dexcom_password = os.getenv("DEXCOM_PASSWORD")
dexcom = pydexcom.Dexcom(dexcom_username, dexcom_password)

glucose_readings = dexcom.get_glucose_readings(minutes=1440, max_count=288)

existing_timestamps = set()