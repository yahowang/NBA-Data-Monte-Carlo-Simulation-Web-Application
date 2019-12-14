from bs4 import BeautifulSoup
from datetime import datetime
import requests
import sched
import os.path

url = 'https://www.basketball-reference.com/leagues/NBA_2020_totals.html'

def _get_file_name(i):
    now = datetime.now()
    return 'data/' + str(now.month) + str(now.day) + '_' + str(i) + '.csv'

def _get_data():
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
    return data


def save_data():
    name = _get_file_name(1)
    i = 2
    while os.path.isfile(name):
        name = _get_file_name(i)
        i += 1

    f = open(name, 'w' ,errors = 'ignore')
    for i in _get_data():
        f.write(','.join(i)+'\n')
    f.close()
    return name

if __name__ == "__main__":
    save_data()
