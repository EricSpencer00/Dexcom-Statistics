import os
from pydexcom import Dexcom
from database import insert_glucose_readings
from defs import get_dexcom_env_variables, get_database_connection

# Initialize variables
dexcom = get_dexcom_env_variables()

# Insert past 24 hours into database
db = get_database_connection()
db_name = os.getenv("sql_database")

try: 
    insert_glucose_readings(dexcom, db, db_name)
finally:
    db.close()