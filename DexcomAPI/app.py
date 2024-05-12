# app.py
'''
Initialize a webapp using Flask
'''
from main import get_dexcom_connection
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_number():
    dexcom = get_dexcom_connection()
    result = dexcom.get_current_glucose_reading()
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug = True)