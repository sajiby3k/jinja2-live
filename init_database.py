import sqlite3

sqlite_file = 'jinja_db.sqlite'    # name of the sqlite database file
templates_table = 'templates'  # name of the table to be created

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS templates")

# Creating a new SQLite table with 1 column
c.execute("""
       CREATE TABLE templates 
                  (path     VARCHAR(32), 
                   name     VARCHAR(32) NOT NULL, 
                   template VARCHAR(32768),
                   params   VARCHAR(1024),
                   timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		   PRIMARY KEY (path, name) )
          """ )



# add  a default  record
c.execute('''
       INSERT INTO templates(path, name,  template, params) VALUES (NULL, "demo", "Hello  {{person.surname}} {{person.name}}!\n{%- if greetings %}\n\n   How are you?\n{%- endif %}\n", "person:\n    name:    Doe\n    surname: John\ngreetings: true\n")
''')
c.execute('''
       INSERT INTO templates(path, name,  template, params) VALUES (NULL, "bgp", "router bgp 65000\n  {%- for neigh in neighs %}\n  neighbor {{ neigh.ip }} remote-as {{ neigh.as }}\n     {%- if neigh.as == 65000 %}\n  neighbor {{ neigh.ip }} next-hop self\n     {%- endif %}\n  {%- endfor %}\n", "neighs: \n    - ip:    10.0.0.1\n      as:    65000\n    - ip:    172.16.0.1\n      as:    65001\n")
''')
# Committing changes and closing the connection to the database file
conn.commit()
conn.close()

