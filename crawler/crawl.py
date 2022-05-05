import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime
#import html5lib

  
URL = "https://www.worldometers.info/coronavirus/"
r = requests.get(URL)
  
soup = BeautifulSoup(r.text, features="lxml") # If this line causes an error, run 'pip install html5lib' or install html5lib

table_body = soup.tbody #Find the table body
data = table_body.findAll('tr')[8:] #Ignore the total rows and start from USA and the last total row

dataframe = []
for i, row in enumerate(data):
    try:
        information = row.findAll('td')[1:] #The first information is index
        item = []
        for j in information:
            item.append(j.text)
        
        dataframe.append(item)
    except:
        continue

dataframe = np.array(dataframe)

columns = ['Country', 'Total Cases', 'New Cases', 
           'Total Deaths', 'New Deaths', 'Total Recovered', 
           'New Recovered', 'Active Cases', 'Serious, Critical', 
           'Total Cases/1M pop', 'Deaths/1M pop', 'Total Tests', 
           'Tests/1M pop', 'Population', 'Continent', 
           '1 Case every X ppl', '1 Death every X ppl', '1 Test every X ppl', 
           'New Cases/1M pop', 'New Deaths/1M pop', 'Active Cases/1M pop']

df = pd.DataFrame(data=dataframe, columns=columns)
date = datetime.today().strftime('%Y-%m-%d')
temp = pd.read_csv('../data/covid.csv')
print(temp)
if date not in temp['Date'].unique():

	df['Date'] = date
	print(df)
	df.to_csv('../data/covid.csv', mode='a', header=False)