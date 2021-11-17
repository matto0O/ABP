from bs4 import BeautifulSoup as Soup
import requests

site_contents = requests.get('https://www.efortuna.pl/zaklady-bukmacherskie/pilka-nozna/ekstraklasa-polska')
site = Soup(site_contents.text, 'lxml')
games = site.findAll('tbody')

for game in games:
    name = (game.find('span', class_='market-name')).text
    date = (game.find('span', class_='event-datetime')).text
    print(name + date)
    odds = game.findAll('span', class_='odds-value')

    oddsFormat = ""

    for enum, x in enumerate(odds):
        oddsFormat += (x.text + " ")
        if enum == 2 or enum == 5:
            print(oddsFormat)
            oddsFormat = ""

    print("===========================")
