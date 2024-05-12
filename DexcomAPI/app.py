# app.py
'''
Initialize a webapp using Flask
'''
from flask import Flask
from main import get_dexcom_connection

app = Flask(__name__)

@app.route('/')
def index():
    dexcom = get_dexcom_connection()
    result = dexcom.get_current_glucose_reading()
    return result

if __name__ == '__main__':
    app.run(debug = True)