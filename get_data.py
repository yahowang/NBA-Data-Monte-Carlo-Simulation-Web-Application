#!pip3 install beautifulsoup4
#!pip3 install requests
#!pip3 install BeautifulSoup4
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
url = 'https://www.basketball-reference.com/leagues/NBA_2020_totals.html'
now = datetime.now()
save_file = 'data/' + str(now.month) + str(now.day) + '.csv'

html_file = requests.get(url)
soup = BeautifulSoup(html_file.text)
table_body = soup.find('tbody')
rows = table_body.find_all('tr')
data = []
feature_names = [row.text.strip() for row in soup.find('thead').find_all("th")]
data.append(feature_names[1:])
for row in rows:
    cols = row.find_all('td')
    if len(cols):
        cols = [element.text.strip() for element in cols]
        data.append([element if element else "NA" for element in cols])

f = open(save_file,'w',errors = 'ignore')

for i in data:
    f.write(','.join(i)+'\n')

f.close()