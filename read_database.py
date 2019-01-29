import sqlite3

sqlite_file = 'jinja_db.sqlite'    # name of the sqlite database file
templates_table = 'templates'  # name of the table to be created

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute("SELECT * from  templates ")
row = c.fetchone()
while row is not None:
  print(row)
  row = c.fetchone()

conn.commit()
conn.close()

