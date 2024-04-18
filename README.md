# DexcomNumberViewer

Display your CGM data to your terminal using Python + Pydexcom!
Optionally, Enter a Twilio Account to send a message to your phone number.

A Dexcom account with a physical CGM and data is required for the program to work.
A Twilio account with working key and messaging number is required for texting support.

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
You will need to install pydexcom and twilio for all features to work.

After Pydexcom is installed you will need to allow your Dexcom's data
to be accessed by Pydexcom's API system.

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

Being a Type 1 Diabetic, a CGM is necessary for my day to day life. 
The Dexcom allows me to see my blood glucose levels throughout the day. 
Things like a Time in Range percentage and A1C estimator keep me alive and help 
make sure I am staying healthy.
Through a sensor on my body, a transmitter reads the level given to it by the sensor
and then transmits the number to my phone using Dexcom's cloud database.
Using Dexcom's g6 mobile app I can see this data, up to 24 hours.
Using Dexcom's Clarity mobile app I can see the data for the past year.
However, I am looking to do more than what the Clarity app does.
I want to learn how my habits, trends, and other factors can influence
my data. As of right now, all I can do is display data, but in the
future I hope to have even more functionality than apps like Sugarmate 
and Clarity




