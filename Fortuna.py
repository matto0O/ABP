from bs4 import BeautifulSoup as Soup
from datetime import datetime as dt
import requests


def findTeams(url):
    site_contents = requests.get(url)
    site = Soup(site_contents.text, 'lxml')
    games = site.find('tbody')

    names = games.findAll('span', class_='market-name')

    returnSet = set()

    for name in names:
        n = name.text.strip().split(" - ")
        returnSet.add(n.__getitem__(0))
        returnSet.add(n.__getitem__(1))

    return returnSet


def insert(cursor, url, competition):
    site_contents = requests.get(url)
    site = Soup(site_contents.text, 'lxml')
    games = site.find('tbody')
    skip = len(games.findAll('div', class_="live-badge"))

    names = games.findAll('span', class_='market-name')
    dates = games.findAll('span', class_='event-datetime')
    oddsAll = games.findAll('span', class_='odds-value')
    today = dt.today()

    for i in range(skip * 6):
        oddsAll.pop(0)

    for e, name in enumerate(names):
        n = name.text.strip().split(" - ")
        date = dates.__getitem__(e).text
        d = date.split("\xa0")
        dateCheck = dt.strptime(d.__getitem__(0) + d.__getitem__(1), "%d.%m.%H:%M")
        date = d.__getitem__(0) + str(today.year + (today < dateCheck)) + d.__getitem__(1)

        # cursor.execute(
        #     "CREATE TABLE IF NOT EXISTS fortuna"
        #     "(host VARCHAR(20) NOT NULL, visitor VARCHAR(20) NOT NULL,"
        #     "date DATETIME NOT NULL, o1 DECIMAL(4,2) NOT NULL, oX DECIMAL(4,2) NOT NULL, o2 DECIMAL(4,2) NOT NULL,"
        #     " o1X DECIMAL(4,2), oX2 DECIMAL(4,2), o12 DECIMAL(4,2), competition VARCHAR(25) NOT NULL,"
        #     " updated TINYINT(1) NOT NULL, visited TINYINT(1) NOT NULL, PRIMARY KEY (host, date, competition))")

        cursor.execute(
            "INSERT INTO games (hostID, visitorID, date, o1, oX, o2, competition, updated, visited, bookie)"
            "VALUES ((SELECT ID FROM teams WHERE fortuna=%s), (SELECT ID FROM teams WHERE fortuna=%s),"
            " STR_TO_DATE(%s, '%d.%m.%Y%H:%i'), %s, %s, %s, %s, 1, 1, 'Fortuna')"
            "ON DUPLICATE KEY UPDATE "
            "updated = IF(o1!=%s or oX!=%s or o2!=%s, 1, 0),"
            "o1=%s, oX=%s, o2=%s, visited = 1",
            (n.__getitem__(0), n.__getitem__(1), date,
             oddsAll.__getitem__(6 * e).text, oddsAll.__getitem__(6 * e + 1).text,
             oddsAll.__getitem__(6 * e + 2).text, competition,

             oddsAll.__getitem__(6 * e).text, oddsAll.__getitem__(6 * e + 1).text,
             oddsAll.__getitem__(6 * e + 2).text,

             oddsAll.__getitem__(6 * e).text, oddsAll.__getitem__(6 * e + 1).text,
             oddsAll.__getitem__(6 * e + 2).text
             ))

