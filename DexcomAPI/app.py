# app.py
'''
Initialize a webapp using Flask
'''
from flask import Flask, render_template, request, redirect, url_for, session
from requests_oauthlib import OAuth2Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from main import get_dexcom_connection, get_sender_email_credentials, get_receiver_email, concise_message_mdgl

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    oauth_token = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cgm_data = db.relationship('CGMData', backref='user', lazy=True)

class CGMData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    glucose_value = db.Column(db.Float, nullable=False)
    system_time = db.Column(db.DateTime, nullable=False)
    display_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Create database tables
@app.before_first_request
def create_tables():
    db.create_all()

# Fetch email credentials
email_username, email_password = get_sender_email_credentials()
receiver_email = get_receiver_email()

# OAuth2 client setup
client_id = os.getenv('DEXCOM_CLIENT_ID')
client_secret = os.getenv('DEXCOM_CLIENT_SECRET')
authorization_base_url = 'https://api.dexcom.com/v2/oauth2/login'
token_url = 'https://api.dexcom.com/v2/oauth2/token'

@app.route('/')
def index():
    if 'oauth_token' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login')
def login():
    dexcom = OAuth2Session(client_id)
    authorization_url, state = dexcom.authorization_url(authorization_base_url)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    dexcom = OAuth2Session(client_id, state=session['oauth_state'])
    token = dexcom.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    session['oauth_token'] = token
    session['user_email'] = dexcom.get('https://api.dexcom.com/v2/users/self').json()['email']
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'oauth_token' not in session:
        return redirect(url_for('index'))

    user = User.query.filter_by(email=session['user_email']).first()
    if not user:
        user = User(email=session['user_email'])
        db.session.add(user)
        db.session.commit()

    token = session['oauth_token']
    dexcom = OAuth2Session(client_id, token=token)
    response = dexcom.get('https://api.dexcom.com/v2/users/self/egvs?startDate=2023-01-01T00:00:00&endDate=2023-01-02T00:00:00')
    data = response.json()
    
    for record in data['egvs']:
        cgm_data = CGMData(
            user_id=user.id,
            glucose_value=record['value'],
            system_time=datetime.fromisoformat(record['systemTime']),
            display_time=datetime.fromisoformat(record['displayTime'])
        )
        db.session.add(cgm_data)
    
    db.session.commit()
    
    cgm_data = CGMData.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', cgm_data=cgm_data)

@app.route('/logout')
def logout():
    session.pop('oauth_token', None)
    session.pop('user_email', None)
    return redirect(url_for('index'))

@app.route('/send-email', methods=['POST'])
def send_email():
    if 'oauth_token' not in session:
        return "Error: Cannot send email without Dexcom connection"
    
    token = session['oauth_token']
    dexcom = OAuth2Session(client_id, token=token)
    
    message = MIMEMultipart()
    message["From"] = email_username
    message["To"] = receiver_email
    message.attach(MIMEText(concise_message_mdgl(dexcom), 'plain'))

    try:
        smtp_server = 'smtp.gmail.com'  # Change this to the appropriate SMTP server if not using Gmail
        smtp_port = 587
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_username, email_password)
            server.sendmail(email_username, receiver_email, message.as_string())
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
