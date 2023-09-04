import sqlite3

conn = sqlite3.connect('northside.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE normal_user (username TEXT UNIQUE, hashed_password TEXT, userid INTEGER PRIMARY KEY)
''')

cursor.execute('''
CREATE TABLE dj_user (dj_username TEXT UNIQUE, dj_hashed_password TEXT, dj_userid INTEGER PRIMARY KEY)
''')

cursor.execute('''
CREATE TABLE Events (EventID INTEGER PRIMARY KEY, EventName TEXT, 
FOREIGN KEY(dj_username) REFERENCES dj_user(dj_username)
FOREIGN KEY(dj_userid) REFERENCES dj_user(dj_userid)
FOREIGN KEY(userid) REFERENCES normal_user(userid)
FOREIGN KEY(username) REFERENCES normal_user(username))
''')


