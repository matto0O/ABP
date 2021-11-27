import mysql.connector

from Fortuna import insert as fortuna
from Sts import insert as sts

database = mysql.connector.connect(
    host="192.168.1.44",
    port="3307",
    user="abp",
    passwd="basedBASED1!",
    db="abp"
)

cursor = database.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS games(host VARCHAR(20), visitor VARCHAR(20), date VARCHAR(17), o1 FLOAT(4,2), oX FLOAT(4,2), o2 FLOAT(4,2), o1X FLOAT(4,2), oX2 FLOAT(4,2), o12 FLOAT(4,2))")

url = 'https://www.efortuna.pl/zaklady-bukmacherskie/pilka-nozna/liga-mistrzow'
fortuna(database, url)
url = "https://www.sts.pl/pl/zaklady-bukmacherskie/pilka-nozna/rozgr-klubowe/liga-mistrzow/184/30856/86428/"
sts(database, url)

database.commit()
