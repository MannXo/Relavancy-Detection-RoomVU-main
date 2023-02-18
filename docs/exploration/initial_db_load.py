import csv
import sqlite3


connection = sqlite3.connect("./RoomVU.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS news (Title text, URL text, Author text, Snippet text, Related int);")
with open(r"train.csv", "r", encoding="utf-8") as fin:
    dr = csv.DictReader(fin)
    to_db = [(i["Title"], i["URL"], i["Author"], i["Snippet"], i["Related"]) for i in dr]

cursor.executemany("INSERT INTO news (Title, URL, Author, Snippet, Related) VALUES (?, ?, ?, ?, ?);", to_db)
connection.commit()
connection.close()
