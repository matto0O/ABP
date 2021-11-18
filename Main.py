from bs4 import BeautifulSoup as Soup
import requests


class Event:
    def __init__(self, name, date, odds):
        self.name = name
        self.date = date
        self.odds = odds

    def to_str(self):
        print(self.name + self.date)
        oddsRows = ""
        for enum, x in enumerate(self.odds):
            oddsRows += (x.text + " ")
            if enum == 2 or enum == 5:
                print(oddsRows)
                oddsRows = ""
        print("=====================")


events_list = []

site_contents = requests.get('https://www.efortuna.pl/zaklady-bukmacherskie/pilka-nozna/ekstraklasa-polska')
site = Soup(site_contents.text, 'lxml')
games = site.find('tbody')

names = games.findAll('span', class_='market-name')
dates = games.findAll('span', class_='event-datetime')
oddsAll = games.findAll('span', class_='odds-value')

for e,name in enumerate(names):
    oddsList = []
    for x in range (6*e, 6*e+6):
        oddsList.append(oddsAll.__getitem__(x))
    newEvent = Event(name.text,dates.__getitem__(e).text,oddsList)
    events_list.append(newEvent)

    events_list.__getitem__(e).to_str()