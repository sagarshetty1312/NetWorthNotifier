# Objective
Reads loan EMI calendar, calculates amount for the day and sends an SMS using Twilio

# Steps for venv
##Create:
virtualenv loan-notification

## Activate:
source loan-notification/bin/activate

## Install dependencies:
pip install -r requirements.txt

## Start:
python3 loan-notification.py

## Deactivate:
deactivate

# Install anacron at /etc/anacrontab
Add the line from anacronfile.txt to the file mentioned above on your computer

# Test anacron
anacron -T

# Set up twilio details as env variables
$TWILIO_ID and $TWILIO_KEY

# Program runs everyday
Depending on the frequency in the anacron file
