import requests
from datetime import date

# Getting today's year, month and day to prepare the url 

today = date.today()
year = today.year
month = today.month
day = today.day

# We convert month from single digit to double digit. For example, 7 to 07.

if day < 10:
    day = '0' + str(day)
else:
    pass

if month < 10:
    month = '0' + str(month)
else:
    pass

# Check if the format for date is correct or not

#print('Year: ' + str(year))
#print('Month: ' + str(month))
#print('Day: ' + str(day) + '\n')

# Creating the URL

cashurl = 'https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_Cash_' + str(day) + '_' + str(month) + '_' + str(year) + '.txt'
fnourl = 'https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_fno_' + str(day) + '_' + str(month) + '_' + str(year) + '.txt'

# Manually check teh URL if there is some issue

#print(cashurl)
#print(fnourl)

# Requesting URL

cash = requests.get(cashurl)
fno = requests.get(fnourl)

# Creating text file and writing data to it

cashfile = open("Cash.txt","w")
fnofile = open('FNO.txt', "w")
cashfile.write(cash.text)
fnofile.write(fno.text)
cashfile.close()
fnofile.close()