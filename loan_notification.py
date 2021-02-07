import os
from datetime import date, datetime
import pandas as pd
import subprocess
from twilio.rest import Client

path = "/home/sagar/Documents/loan_notification"

#Get difference in days
def dateDiff(date1, date2):
    return (date1 - date2).days

#Get datetime object assuming string is in dd/mm/yy format
def getDate(dateStr):
    return datetime.strptime(dateStr, "%d/%m/%y")

#Get int amount from string with commas
def getIntFromStr(strWithCommas):
    return int(float(strWithCommas.replace(',','')))

#Get number as comma formatted string
def toCommaFormat(num):
    return '{:,}'.format(num)

#Read xlsx file (Needs openpyxl)
fileName = "Repayment_Calendar.xlsx"
df = pd.read_excel(path +"/"+ fileName)
dateToday = datetime.today()

#Find the date just before today
index = 0
tempDate = getDate(df['Date'][index])

while dateDiff(tempDate, dateToday) <= 0:
    index += 1
    tempDate = getDate(df['Date'][index])

prevDate = getDate(df['Date'][index - 1])
nextDate = getDate(df['Date'][index])

prevPrincipal = getIntFromStr(df['Prn.O/S'][index - 1])
nextPrincipal = getIntFromStr(df['Prn.O/S'][index])
gainPerDay = abs((prevPrincipal - nextPrincipal) / dateDiff(prevDate, nextDate))
gainPerDay = int(gainPerDay)

resultForToday = prevPrincipal + abs(dateDiff(prevDate, dateToday)) * gainPerDay
resultForYesterday = resultForToday - gainPerDay
result = f"""Principal Now: Rs. {toCommaFormat(resultForToday)}
Principal Yesterday: Rs. {toCommaFormat(resultForYesterday)}
Net Increase: Rs. {toCommaFormat(gainPerDay)}"""

print(result)

# subprocess.run(["notify-send", "--icon=error", "Loan Notification", f"""Principal Now: Rs. {toCommaFormat(resultForToday)}
# Principal Yesterday: Rs. {toCommaFormat(resultForYesterday)}
# Net Increase: Rs. {toCommaFormat(gainPerDay)}"""])

#Twilio API
client = Client(os.getenv("TWILIO_ID"), os.getenv("TWILIO_KEY"))
client.messages.create(to="+13528713765", from_="+13852826464", body=result)
