from bs4 import BeautifulSoup as Soup
import requests


def insert(database, url):
    cursor = database.cursor()

    site_contents = requests.get(url)
    site = Soup(site_contents.text, 'lxml')
    games = site.findAll('div', class_='bet_tab')
    inner_sites = games.__getitem__(0).findAll('td', class_='date_time')

    for inner in inner_sites:
        desired_site = Soup(requests.get('https://www.sts.pl' + (inner.find('a')['href'])).text, 'lxml')
        header = desired_site.find('a', class_='openMenu').text.strip().split(" - ")
        oddsFiltered = list(filter(lambda x: x != '', desired_site.find('table', class_='col3').text.split("\n")))
        cursor.execute("INSERT INTO games (host, visitor, date, o1, oX, o2, o1X, oX2, o12) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (header.__getitem__(0), header.__getitem__(1),
                        header.__getitem__(2).split(" ").__getitem__(1) + " " + header.__getitem__(3),
                        oddsFiltered.__getitem__(2), oddsFiltered.__getitem__(4),
                        oddsFiltered.__getitem__(6), oddsFiltered.__getitem__(9),
                        oddsFiltered.__getitem__(11), oddsFiltered.__getitem__(13)))
