# database.py
import datetime
import mysql.connector
import pydexcom
import os
from defs import get_dexcom_connection, get_database_connection

def get_latest_timestamp(cursor):
    query = "SELECT MAX(timestamp) FROM dexcom_data"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result[0] is not None else None

def insert_glucose_readings(dexcom, db):
    cursor = db.cursor()

    latest_timestamp = get_latest_timestamp(cursor)

    glucose_readings = dexcom.get_glucose_readings(minutes=1440, max_count=288)

    insert_data = []

    now = datetime.datetime.now()
    base_minute = now.minute - (now.minute % 5)
    base_timestamp = now.replace(minute=base_minute, second=0, microsecond=0)

    for index in reversed(range(len(glucose_readings))):
        reading = glucose_readings[index]
        timestamp = base_timestamp - datetime.timedelta(minutes=index * 5)

        # Ensure timestamps will not overlap and duplicate data in table
        if latest_timestamp is None or timestamp > latest_timestamp:
            mgdl_reading = reading.value
            insert_data.append((timestamp, mgdl_reading))

    if insert_data:
        cursor.executemany("INSERT INTO dexcom_data (timestamp, mgdl_reading) VALUES (%s, %s)", insert_data)
        db.commit()

    cursor.close()

def main():
    dexcom = get_dexcom_connection()
    db = get_database_connection()

    try: 
        insert_glucose_readings(dexcom, db)
    finally:
        db.close()
