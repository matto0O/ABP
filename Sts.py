from bs4 import BeautifulSoup as Soup
import requests


def findTeams(url):
    site_contents = requests.get(url)
    site = Soup(site_contents.text, 'lxml')
    games = site.findAll('div', class_='bet_tab')
    teams = games.__getitem__(0).findAll('a')

    returnSet = set()

    for e, team in enumerate(teams):
        try:
            returnSet.add(teams.__getitem__(e * 7 + 1).text.split("\n").__getitem__(1).strip())
            returnSet.add(teams.__getitem__(e * 7 + 3).text.split("\n").__getitem__(1).strip())
        except IndexError:
            break

    return returnSet


def insert(cursor, url, competition):
    site_contents = requests.get(url)
    site = Soup(site_contents.text, 'lxml')
    games = site.findAll('div', class_='bet_tab')
    try:
        inner_sites = games.__getitem__(0).findAll('td', class_='date_time')
        for inner in inner_sites:
            desired_site = Soup(requests.get('https://www.sts.pl' + (inner.find('a')['href'])).text, 'lxml')
            header = desired_site.find('a', class_='openMenu').text.strip().split(" - ")
            oddsFiltered = list(filter(lambda x: x != '' and x != " ", desired_site.find('table', class_='col3').text.split("\n")))

            # cursor.execute(
            #     "CREATE TABLE IF NOT EXISTS sts"
            #     "(host VARCHAR(20) NOT NULL, visitor VARCHAR(20) NOT NULL,"
            #     "date DATETIME NOT NULL, o1 DECIMAL(4,2) NOT NULL, oX DECIMAL(4,2) NOT NULL, o2 DECIMAL(4,2) NOT NULL,"
            #     " o1X DECIMAL(4,2), oX2 DECIMAL(4,2), o12 DECIMAL(4,2), competition VARCHAR(25) NOT NULL,"
            #     "updated TINYINT(1) NOT NULL, visited TINYINT(1) NOT NULL, PRIMARY KEY (host, date, competition))")

            cursor.execute(
                "INSERT INTO games (hostID, visitorID, date, o1, oX, o2, o1X, oX2, o12, competition, updated, visited, bookie) "
                "VALUES ((SELECT ID FROM teams WHERE sts=%s), (SELECT ID FROM teams WHERE sts=%s), "
                "STR_TO_DATE(%s, '%d.%m.%Y%H:%i'), %s, %s, %s, %s, %s, %s, %s, 1, 1, 'STS')"
                "ON DUPLICATE KEY UPDATE "
                "updated = IF(o1!=%s or oX!=%s or o2!=%s or o1X!=%s or oX2!=%s or o12!=%s, 1, 0),"
                "o1=%s, oX=%s, o2=%s, o1X=%s, oX2=%s, o12=%s, visited = 1",
                (header.__getitem__(0), header.__getitem__(1),
                 header.__getitem__(2).split(" ").__getitem__(1) + header.__getitem__(3),
                 oddsFiltered.__getitem__(2), oddsFiltered.__getitem__(4),
                 oddsFiltered.__getitem__(6), oddsFiltered.__getitem__(9),
                 oddsFiltered.__getitem__(11), oddsFiltered.__getitem__(13),
                 competition,

                 oddsFiltered.__getitem__(2), oddsFiltered.__getitem__(4),
                 oddsFiltered.__getitem__(6), oddsFiltered.__getitem__(9),
                 oddsFiltered.__getitem__(11), oddsFiltered.__getitem__(13),

                 oddsFiltered.__getitem__(2), oddsFiltered.__getitem__(4),
                 oddsFiltered.__getitem__(6), oddsFiltered.__getitem__(9),
                 oddsFiltered.__getitem__(11), oddsFiltered.__getitem__(13)
                 ))
    except IndexError:
        return False
    return True

