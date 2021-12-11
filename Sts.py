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
    try:
        games = site.findAll('div', class_='bet_tab').__getitem__(0)
        labels = games.findAll('table', class_='col3')
        date = ""
        for enum, label in enumerate(labels):
            subLabel = label.text.replace('\xa0','\n').split("\n")
            l = list(filter(lambda x: (x != '' and x != ' '),subLabel))
            sus = l.__getitem__(0)
            if ':' in sus:
                cursor.execute(
                    "INSERT INTO games (hostID, visitorID, date, o1, oX, o2, competition, updated, visited, bookie) "
                    "VALUES ((SELECT ID FROM teams WHERE sts=%s), (SELECT ID FROM teams WHERE sts=%s), "
                    "STR_TO_DATE(%s, '%d.%m.%Y%H:%i'), %s, %s, %s, %s, 1, 1, 'STS')"
                    "ON DUPLICATE KEY UPDATE "
                    "updated = IF(o1!=%s or oX!=%s or o2!=%s, 1, 0),"
                    "o1=%s, oX=%s, o2=%s, visited = 1",
                    (l.__getitem__(1).lstrip(), l.__getitem__(5).lstrip(),
                     date + sus,
                     l.__getitem__(2), l.__getitem__(4),
                     l.__getitem__(6), competition,

                     l.__getitem__(2), l.__getitem__(4),
                     l.__getitem__(6),

                     l.__getitem__(2), l.__getitem__(4),
                     l.__getitem__(6)
                ))
            else:
                date = l.__getitem__(3).split(" ").__getitem__(1)
                cursor.execute(
                    "INSERT INTO games (hostID, visitorID, date, o1, oX, o2, competition, updated, visited, bookie) "
                    "VALUES ((SELECT ID FROM teams WHERE sts=%s), (SELECT ID FROM teams WHERE sts=%s), "
                    "STR_TO_DATE(%s, '%d.%m.%Y%H:%i'), %s, %s, %s, %s, 1, 1, 'STS')"
                    "ON DUPLICATE KEY UPDATE "
                    "updated = IF(o1!=%s or oX!=%s or o2!=%s, 1, 0),"
                    "o1=%s, oX=%s, o2=%s, visited = 1",
                    (l.__getitem__(5).lstrip(), l.__getitem__(9).lstrip(),
                     date + l.__getitem__(4),
                     l.__getitem__(6), l.__getitem__(8),
                     l.__getitem__(10), competition,

                     l.__getitem__(6), l.__getitem__(8),
                     l.__getitem__(10),

                     l.__getitem__(6), l.__getitem__(8),
                     l.__getitem__(10)
                     ))
        return True
    except IndexError:
        return False
