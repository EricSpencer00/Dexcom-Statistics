# DexcomNumberViewer

Display your CGM data to your terminal using Python + Pydexcom!
Optionally, Enter a Twilio Account to send a message to your phone number

A Dexcom account with a physical CGM and data is required for the program to work
A Twilio account with working key and messaging number is required for texting support

## Instructions
Create an .env file with your Dexcom and Twilio credentials like so:
```
DEXCOM_USERNAME=username
DEXCOM_PASSWORD=password
```
```
TWILIO_FROM=+1[Twilio phone number here]
TWILIO_TO=+1[Your phone number here]

account_sid=[Your Twilio account number here]
auth_token=[Your API Key here]
```
You will need to install pydexcom and twilio for all features to work

If you do not have Twilio, you can delete all relational code for sole Terminal support
```
pip3 install pydexcom
```
```
pip3 install twilio
```

After you have made your .env file, place it in the same working directory as the Python file and you are good to go

Example Output:
```
Your current glucose level is 136 mg/dL (steady →)
Time of reading: 2024-04-18 13:07:31
Glucose state: In Range
Average glucose level: 141.5451 mg/dL
Estimated A1C: 9.484
Time in Range (70-150 mg/dL): 58.33%
```

## Background information

Being a Type 1 Diabetic, a CGM is necessary for my day to day life


