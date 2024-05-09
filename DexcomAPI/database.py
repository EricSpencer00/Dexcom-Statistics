import datetime
import mysql.connector
import pydexcom
import os


dexcom_username = os.getenv("DEXCOM_USERNAME")
dexcom_password = os.getenv("DEXCOM_PASSWORD")
dexcom = pydexcom.Dexcom(dexcom_username, dexcom_password)

db = mysql.connector.connect(
    host = os.getenv("sql_host"),
    user = os.getenv("sql_user"),
    password = os.getenv("sql_password"),
    database = os.getenv("sql_database")
)

def get_latest_timestamp(cursor):
    query = "SELECT MAX(timestamp) FROM dexcom_data"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result[0] is not None else None

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
db.close()
