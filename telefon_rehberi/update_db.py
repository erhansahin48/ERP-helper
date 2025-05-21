import sqlite3

conn = sqlite3.connect('rehber.db')  # doğru yolu kullan
cur = conn.cursor()

cur.execute("PRAGMA table_info(yemek_listesi)")
columns = cur.fetchall()

for col in columns:
    print(f"{col[1]} ({col[2]})")

conn.close()
