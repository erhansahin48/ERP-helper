import sqlite3

conn = sqlite3.connect('rehber.db')  # Veritabanı dosyası
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS yemekler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tarih TEXT NOT NULL,
    menu TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("Tablo oluşturuldu veya zaten mevcut.")
