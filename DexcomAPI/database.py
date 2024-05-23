# database.py
# make sure you are in the correct Database

import datetime
import mysql.connector
import pydexcom
import os
from mysql.connector import Error
from defs import get_dexcom_connection, get_database_connection

def get_latest_timestamp(cursor, db_name):
    try:
        query = f"SELECT MAX(timestamp) FROM {db_name}"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result[0] is not None else None
    except Error as e:
        print(f"Error: ", e)
        return None

def get_latest_notification(db, db_name):

    cursor = db.cursor()

    try:
        create_temp_table_query = f"CREATE TEMPORARY TABLE latest_timestamp_temp AS SELECT MAX(timestamp) AS latest_timestamp FROM {db_name}"
        cursor.execute(create_temp_table_query)

        notification_query = f"SELECT notification FROM {db_name} WHERE timestamp IN (SELECT latest_timestamp FROM latest_timestamp_temp)"
        cursor.execute(notification_query)
        latest_notification = cursor.fetchone()[0]

        timestamp_query = f"SELECT timestamp FROM {db_name} ORDER BY timestamp DESC LIMIT 6"
        cursor.execute(timestamp_query)
        latest_timestamps = [row[0] for row in cursor.fetchall()]

        return latest_notification, latest_timestamps
    except Error as e:
        print(f"Error: ", e)
        return None, None
    finally:
        drop_temp_table_query = "DROP TEMPORARY TABLE IF EXISTS latest_timestamp_temp"
        cursor.execute(drop_temp_table_query)


def insert_glucose_readings(dexcom, db, db_name):
    
    cursor = db.cursor()
    
    try:

        latest_timestamp = get_latest_timestamp(cursor, db_name)

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
                insert_data.append((timestamp, mgdl_reading, 0))

        if insert_data:
            cursor.executemany(f"INSERT INTO {db_name} (timestamp, mgdl_reading, notification) VALUES (%s, %s, %s)", insert_data)
            db.commit()

        cursor.close()
    except Error as e:
        print(f"Error: ", e)
        db.rollback()
        cursor.close()