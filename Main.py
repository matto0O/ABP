import mysql.connector
import pandas as pd

from Finder import addNamesToDatabase
import time
import Fortuna
import Sts

database = mysql.connector.connect(
    host="192.168.1.44",
    port="3307",
    user="abp",
    passwd="basedBASED1!",
    db="abp"
)

timeS = time.time()

cursor = database.cursor()

# cursor.execute(
#     "CREATE TABLE IF NOT EXISTS games"
#     "(hostID INT, visitorID INT NOT NULL,"
#     "date DATETIME, o1 DECIMAL(4,2) NOT NULL, oX DECIMAL(4,2) NOT NULL, o2 DECIMAL(4,2) NOT NULL,"
#     " o1X DECIMAL(4,2), oX2 DECIMAL(4,2), o12 DECIMAL(4,2), competition VARCHAR(25) NOT NULL,"
#     "updated TINYINT(1) NOT NULL, visited TINYINT(1) NOT NULL, bookie VARCHAR(12) NOT NULL,"
#     " PRIMARY KEY (hostID, date, bookie))")

cursor.execute("UPDATE games SET updated = 0, visited = 0")

df_Fortuna = pd.read_csv("fortunacsv.txt")
df_Sts = pd.read_csv("stscsv.txt")

for e in range(df_Sts.__len__()):
    # addNamesToDatabase(
    #     sorted(Fortuna.findTeams(df_Fortuna.iloc[e].__getitem__(0)), key=(lambda string: len(string)), reverse=True),
    #     sorted(Sts.findTeams(df_Sts.iloc[e].__getitem__(0)), key=(lambda string: len(string)), reverse=True), cursor
    # )
    if not Sts.insert(cursor, df_Sts.iloc[e].__getitem__(0), df_Sts.iloc[e].__getitem__(1)):
        continue
    Fortuna.insert(cursor, df_Fortuna.iloc[e].__getitem__(0), df_Fortuna.iloc[e].__getitem__(1))

cursor.execute("DELETE FROM games WHERE date < now() or visited = 0")

# cursor.execute("CREATE TABLE IF NOT EXISTS arbitrage"
#                 "(hostID INT, visitorID INT,"
#                 "date DATETIME, o1 DECIMAL(4,2) NOT NULL, oX DECIMAL(4,2) NOT NULL, o2 DECIMAL(4,2) NOT NULL,"
#                 " o1X DECIMAL(4,2), oX2 DECIMAL(4,2), o12 DECIMAL(4,2), competition VARCHAR(25) NOT NULL,"
#                 " PRIMARY KEY (hostID, visitorID, date))")

cursor.execute("TRUNCATE TABLE arbitrage")

cursor.execute("INSERT INTO arbitrage SELECT hostID, visitorID, date,"
               " MAX(`o1`), MAX(`oX`), MAX(`o2`), MAX(`o1X`), MAX(`oX2`), MAX(`o12`), competition"
               " FROM games GROUP BY hostID, visitorID, date")

cursor.execute("DELETE FROM arbitrage WHERE (1/o1+1/o2+1/oX>=1)"
               " and (1/o1+1/oX2>=1) and (1/oX+1/o12>=1) and (1/o2+1/o1X>=1)")

database.commit()

print(str(time.time() - timeS))
