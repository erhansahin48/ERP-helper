import sqlite3

def init_db():
    conn = sqlite3.connect('telefon_rehberi.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS duyurular (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        baslik TEXT NOT NULL,
        icerik TEXT NOT NULL,
        tarih TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Veritabanı ve tablo oluşturuldu.")
