import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
from random import uniform
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import schedule

# This scraper grabs paginated data from the player marketplace of an old game.
# It runs every 30 minutes. It is good for searching for historic volume/price data.

# Using pandas, I can do several things. 
# I can find out which characters are logging in and out between scrapes.
# Although there are no flags given for when a character has sold an item, I can 
# predict whether an item has sold or not, reinforcing my figured demand price for a given item.
# (Simply taking the average of the list prices for an item isn't accurate)
# I have not provided the URL to protect the servers (and my technique). Maybe you can ask me about it :)

app = Flask(__name__)

# My persistent DB
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///./prod.db'

# DB used druing testing/development
#app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///./dev.db'

db = SQLAlchemy(app)

class Entry(db.Model):
    def __init__(self, character, item, price, page_number, page_datetime, batch_number, batch_datetime):
        self.character = character
        self.item = item
        self.price = price
        self.page_number = page_number
        self.page_datetime = page_datetime
        self.batch_number = batch_number
        self.batch_datetime = batch_datetime

    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.String(120), unique=False, nullable=False)
    item = db.Column(db.String(120), unique=False, nullable=False)
    price = db.Column(db.String(40), unique=False, nullable=False)
    page_number = db.Column(db.Integer, unique=False)
    page_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    batch_number = db.Column(db.Integer, unique=False)
    batch_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<item: {self.item}, character: {self.character}, price: {self.price}>'

db.create_all()

def do_run():
    if Entry.query.order_by(Entry.id).count()>=1:
        batch_number = Entry.query.order_by(Entry.id)[-1].batch_number + 1
    else:
        batch_number = 1
    batch_datetime = datetime.now()
    url = 'askme'
    debug_pagination_start = 0
    with requests.Session() as session:
        pagination=debug_pagination_start
        offsetPagination = False
        while True:
            pagination = pagination - int(offsetPagination)
            print(f"Requesting page for pagination {pagination}")
            r = session.get(url.format(pagination))
            page = BeautifulSoup(r.content, 'lxml')
            if (page.contents==[]) or (re.search(r'404 Not Found', page.text)):
                # There are some problems with empty content responses althoug still status 200.
                # It is a problem with global state of their server, 
                # where that pagination becomes unavailable for a couple minutes.
                # To fix this, I just request a pagination window overlapping
                # with one already reviewed item (from the last page).
                # I don't like it, but seems problem isn't on my end.
                print(f"Empty or bad page found at pagination {pagination}")
                offsetPagination = True
            else:
                pagination = processPage(page, pagination, batch_number, batch_datetime, offsetPagination)
                offsetPagination = False
            if not pagination:
                return
        return

def processPage(page, pagination, batch_number, batch_datetime, offsetPagination=False):
    page_datetime = datetime.now()
    page_number = int(pagination / 25 + 1)

    item_table = page.find_all("table")[-1]
    items = item_table.find_all("tr", {"onmouseout": re.compile(r".*")})
    if offsetPagination==True:
        items.pop(0)
    for item in items:
        item_name = item.find_all("td")[0].text
        item_price = item.find_all("td")[1].text
        match = re.search(r'((?P<pp>\d+)p )?((?P<sp>\d+)s )?((?P<gp>\d+)g )?((?P<cp>\d+)c )?', item_price)
        pp = match.group('pp') if match.group('pp') else '0'
        gp = match.group('gp') if match.group('gp') else '0'
        sp = match.group('sp') if match.group('sp') else '0'
        cp = match.group('cp') if match.group('cp') else '0'
        item_price = pp + "." + gp + sp + cp
        item_seller = item.find_all("td")[2].text
        entry = Entry(item_seller, item_name, item_price,
                      page_number, page_datetime,
                      batch_number, batch_datetime)
        db.session.add(entry)
        print(f"scraped {entry}")
    db.session.commit()
    nav_links = item_table.find("td", {"valign": "bottom"}).find_all("a")
    if nav_links[-1].text == 'Next':
        wait(pagination, 4, 10.5)
        pagination = pagination + 25
        return pagination
    else:
        return False

def wait(pagination, lower, upper):
    wait = uniform(lower, upper)
    print(f"Finished pagination val: {pagination}. Waiting {wait} seconds")
    sleep(wait)


do_run()
print(f"Beginning Batch: {datetime.now()}")
def job():
    print(f"Beginning Job: {datetime.now()}")
    do_run()
    print(f"Finished Job: {datetime.now()}")

schedule.every(30).minutes.do(job)

while True:
    schedule.run_pending()
    sleep(5)
