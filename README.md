## main.py:

Display your CGM data to your terminal using Python + Pydexcom!
Optionally, Enter a Twilio API Key to send a message to your phone number.

A Dexcom account with a physical CGM and data is required for the program to work.
A Twilio account with working key and messaging number is required for text alert support.

## Instructions
Create an .env file with your Dexcom and Twilio credentials like so:
```
DEXCOM_USERNAME=username
DEXCOM_PASSWORD=password
```
```
TWILIO_FROM=+[Twilio phone number here]
TWILIO_TO=+[Your phone number here]

account_sid=[Your Twilio account number here]
auth_token=[Your API Key here]
```
Note the '+' before the area code to the right of your number.

After you have made your .env file, place it in the same working directory as the Python file.

You will need to allow your Dexcom's data
to be accessed by Pydexcom's API system.
Pydexcom only works using the Dexcom Share feature.

To do this:
- Make sure you have at least one follower on Dexcom Share, this can be yourself on a different account
- If your account is newer, you may use an email in place of a username, make sure you know which type you account is
- Then, make sure you are sharing the credentials for your Dexcom account, not the follower's account
- You will need to make sure your password is not only numbers, as this will cause Pydexcom to not recognize your password

You will need to install pydexcom and twilio for all features to work.

If you do not have a Twilio API Key, you can delete all Twilio-related code and just have Terminal support
```
pip3 install pydexcom
```
```
pip3 install twilio
```

Example Output:
```
Your current glucose level is 144 mg/dL (steady →)
Time of reading: 2024-04-28 17:17:48
Glucose state: In Range
Average glucose level: 140.0242 mg/dL
Estimated A1C: 9.3996
Time in Range (70-150 mg/dL): 50.81%
Median Glucose: 138.5 mg/dL
Standard Deviation: 54.5062 mg/dL
Minimum Glucose: 39 mg/dL
Maximum Glucose: 249 mg/dL
Glucose Range: 210 mg/dL
Coef. of Variation: 38.9263%
Glycemic Variability Index: 98.64072441980657%
```

## arima.py

Predict the next values of your Dexcom graph!

Make sure your Dexcom credentials are in an .env file like before.

Install pydexcom, pandas, numpy, and skikit-learn for this script to work

```
pip3 install pydexcom scikit-learn pandas numpy
```

Example Output:
```
Current time: 11:37PM (CDT) - Trend: falling: 124.30

Predicting future glucose levels...
11:42PM (CDT) - Trend: falling: 120.93
11:47PM (CDT) - Trend: falling: 117.55
11:52PM (CDT) - Trend: falling: 114.18
11:57PM (CDT) - Trend: falling: 110.81
12:02AM (CDT) - Trend: falling: 107.43
12:07AM (CDT) - Trend: falling: 104.06
12:12AM (CDT) - Trend: falling: 100.69
12:17AM (CDT) - Trend: falling: 97.31
```
This information is based solely on data, and does not incorporate factors like insulin/carb correction. It's a good predictor of what would happen to you if you didn't do anything based on your current trends. The program takes the 20 previous points and predicts the next readings based on linear regression.

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




