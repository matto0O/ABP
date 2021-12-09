import mysql.connector
import csv
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
#     "CREATE TABLE IF NOT EXISTS games(host VARCHAR(20) NOT NULL, visitor VARCHAR(20) NOT NULL,"
#     " date DATETIME NOT NULL,"
#     " o1 FLOAT(4,2) FOREIGN KEY NOT NULL, oX FLOAT(4,2) FOREIGN KEY NOT NULL, o2 FLOAT(4,2) FOREIGN KEY NOT NULL,"
#     " o1X FLOAT(4,2) FOREIGN KEY, oX2 FLOAT(4,2) FOREIGN KEY, o12 FLOAT(4,2) FOREIGN KEY,"
#     " competition VARCHAR(25) NOT NULL)")

fortunaSet = set()
stsSet = set()

df_Fortuna = pd.read_csv("fortunacsv.txt")
df_Sts = pd.read_csv("stscsv.txt")

print(df_Sts)

for e in range(df_Sts.__len__()):
    if e == 0:
        continue
    fortunaList = sorted(Fortuna.findTeams(df_Fortuna.iloc[e].__getitem__(0)), key=(lambda string: len(string)), reverse=True)
    stsList = sorted(Sts.findTeams(df_Sts.iloc[e].__getitem__(0)), key=(lambda string: len(string)), reverse=True)
    addNamesToDatabase(fortunaList,stsList,cursor)

database.commit()

# #         Fortuna.insert(cursor, x.__getitem__(0), x.__getitem__(1))
# # Fortuna.deletePast(cursor)
# # database.commit()
#

#         Sts.insert(cursor, x.__getitem__(0), x.__getitem__(1))
# Sts.deletePast(cursor)
# database.commit()

print(str(time.time() - timeS))
