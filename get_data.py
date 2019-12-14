from bs4 import BeautifulSoup
from datetime import datetime
import requests
import sched
import time
import database
from database import upsert_nba
import pandas as pds

url = 'https://www.basketball-reference.com/leagues/NBA_2020_totals.html'
DOWNLOAD_PERIOD = 30    # 30 seconds
counting = 1

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

def update_data_once():
    file_name = 'data/data.csv'
    f = open(file_name, 'w' ,errors = 'ignore')
    for i in _get_data():
        f.write(','.join(i)+'\n')
    f.close()

    df = pds.read_csv(file_name)
    upsert_nba(df)
    global counting
    print("Fectching Data", counting, 'time')
    counting += 1

def main_loop(timeout = DOWNLOAD_PERIOD):
    scheduler = sched.scheduler(time.time, time.sleep)

    def _worker():
        update_data_once()
        scheduler.enter(timeout, 1, _worker)

    scheduler.enter(0, 1, _worker) # start the first event
    scheduler.run(blocking=True)

if __name__ == "__main__":
    main_loop()
    
