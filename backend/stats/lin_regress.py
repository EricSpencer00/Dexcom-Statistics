import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import datetime
from defs import get_database_connection

db_connection = get_database_connection()

query = "SELECT timestamp, mgdl_reading FROM Dexcom_Values"
df = pd.read_sql(query, db_connection)

db_connection.close()

df['timestamp'] = pd.to_datetime(df['timestamp'])
df['timestamp'] = df['timestamp'].astype(np.int64) // 10**9  # Convert to seconds since epoch

X = df[['timestamp']]
y = df['mgdl_reading']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

last_timestamp = df['timestamp'].iloc[-1]
next_timestamps = np.array([last_timestamp + i*300 for i in range(1, 6)]).reshape(-1, 1)  # 5-minute intervals

predictions = model.predict(next_timestamps)
next_datetimes = [datetime.datetime.fromtimestamp(ts[0]) for ts in next_timestamps]

for dt, pred in zip(next_datetimes, predictions):
    print(f"Predicted mg/dL at {dt}: {pred:.2f}")
