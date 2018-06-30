from config import database
import sqlite3

conn = sqlite3.connect(database)
c = conn.cursor()

# Use this file in case you want to create a new database, clean up the old one,
# make sure the database is formatted correctly or delete all current data.
# Do not execute if the database contains information you do not want to lose.

print("Are you sure you want to reformat the database? All data will be lost, and it cannot be restored!")
print("Tip: If you want a new database without destroying the old one, create a new file with the .db extension and use that one.")
if input("If you still want to reformat the database, please type YES to continue.") == "YES":
    c.execute("DROP TABLE IF EXISTS 'users'")
    c.execute("CREATE TABLE 'users' ('id' TEXT NOT NULL, 'name' TEXT, 'spam_activity' REAL NOT NULL DEFAULT 0, 'activity' REAL NOT NULL DEFAULT 0, 'spam_filter' INTEGER NOT NULL DEFAULT 500 PRIMARY KEY(`id`));")
    print("The file {} has been formatted successfully and is now ready to be used!".format(database))
else:
    print("Formatting canceled.")
