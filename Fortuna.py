from bs4 import BeautifulSoup as Soup
from datetime import date as dt
import requests


def insert(database, url):
    cursor = database.cursor()

    site_contents = requests.get(url)
    site = Soup(site_contents.text, 'lxml')
    games = site.find('tbody')

    names = games.findAll('span', class_='market-name')
    dates = games.findAll('span', class_='event-datetime')
    oddsAll = games.findAll('span', class_='odds-value')

    today = dt.today()

    for e, name in enumerate(names):
        n = name.text.strip().split(" - ")
        date = dates.__getitem__(e).text
        d = date.split("\xa0")
        date = d.__getitem__(0) + str(today.year + (today.strftime("%d.%m. %H:%M") < date)) + " " + d.__getitem__(1)

        cursor.execute("INSERT INTO games (host, visitor, date, o1, oX, o2, o1X, oX2, o12) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (n.__getitem__(0), n.__getitem__(1), date,
                        oddsAll.__getitem__(6 * e).text, oddsAll.__getitem__(6 * e + 1).text,
                        oddsAll.__getitem__(6 * e + 2).text, oddsAll.__getitem__(6 * e + 3).text,
                        oddsAll.__getitem__(6 * e + 4).text, oddsAll.__getitem__(6 * e + 5).text))
