from bs4 import BeautifulSoup
from datetime import datetime
import requests
import sched
import time
import database
from database import upsert_nba

url = 'https://www.basketball-reference.com/leagues/NBA_2020_totals.html'
DOWNLOAD_PERIOD = 30    # 30 seconds
COUNTING = 1

def _get_data():
    '''Fetches the data from html and returns a list of dictionary containing records'''
    html_file = requests.get(url)
    soup = BeautifulSoup(html_file.text)
    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')
    data = [] # a list of records.
    feature_names = [row.text.strip() for row in soup.find('thead').find_all("th")]
    rank = 1
    for r in rows:
        cols = r.find_all('td')
        if len(cols):
            cols = [element.text.strip() for element in cols]
            cols = [str(rank)] + [element if element else '0' for element in cols]   
            rank += 1
            record = dict() # store the record for this player
            for i in range(len(feature_names)):
                record[feature_names[i]] = cols[i]
            data.append(record)
    return data

def update_data_once():
    global COUNTING
    data = _get_data()
    upsert_nba(data)
    print("Fectching Data", COUNTING, 'times')
    COUNTING += 1

def main_loop(timeout = DOWNLOAD_PERIOD):
    scheduler = sched.scheduler(time.time, time.sleep)

    def _worker():
        update_data_once()
        scheduler.enter(timeout, 1, _worker)

    scheduler.enter(0, 1, _worker) # start the first event
    scheduler.run(blocking=True)

if __name__ == "__main__":
    main_loop()
