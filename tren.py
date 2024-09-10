import sqlite3
con = sqlite3.connect('sample.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS popa(title, country, region)")
res = cur.execute("SELECT name FROM sqlite_master")
res.fetchone()
print(res)
cur.execute('''INSERT INTO popa VALUES
        ('Sharipovo', 'Russia', '124'),
        ('Kemerovo', 'Russia', '42')''')
con.commit()
res = cur.execute("SELECT region FROM popa")
a = res.fetchall()
print(a)