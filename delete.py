import sqlite3

conn=sqlite3.connect('reservation.db')
c=conn.cursor()
c.execute