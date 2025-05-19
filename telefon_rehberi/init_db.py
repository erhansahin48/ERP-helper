import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    conn = sqlite3.connect('rehber.db')
    c = conn.cursor()

    # Kisiler tablosu
    c.execute('''
        CREATE TABLE IF NOT EXISTS kisiler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            departman TEXT NOT NULL,
            dahili TEXT NOT NULL,
            email TEXT,
            cep TEXT
        )
    ''')

    # Kullanicilar tablosu
    c.execute('''
        CREATE TABLE IF NOT EXISTS kullanicilar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Duyurular tablosu
    c.execute('''
        CREATE TABLE IF NOT EXISTS duyurular (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            baslik TEXT NOT NULL,
            icerik TEXT NOT NULL
        )
    ''')

    # Yemek listesi tablosu
    c.execute('''
        CREATE TABLE IF NOT EXISTS yemek_listesi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarih TEXT NOT NULL,
            menu TEXT NOT NULL
        )
    ''')
    
 


    # Admin kullanıcıyı ekle (varsa tekrar eklemez)
    c.execute("SELECT * FROM kullanicilar WHERE username = 'admin'")
    if not c.fetchone():
        hashed_pw = generate_password_hash('sifre123')
        c.execute("INSERT INTO kullanicilar (username, password) VALUES (?, ?)", ('admin', hashed_pw))

    conn.commit()
    conn.close()
    print("Veritabanı ve tablolar oluşturuldu, admin kullanıcı eklendi (şifre: sifre123)")

if __name__ == "__main__":
    init_db()

