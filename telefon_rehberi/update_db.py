import sqlite3

def update_database():
    conn = sqlite3.connect('telefon_rehberi.db')  # Veritabanı dosyanı buraya yaz
    cursor = conn.cursor()

    # Eğer varsa eski tabloyu sil
    cursor.execute('DROP TABLE IF EXISTS yemekler')

    # Yeni tabloyu oluştur (id, tarih, yemek1 - yemek5)
    cursor.execute('''
    CREATE TABLE yemekler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarih TEXT NOT NULL,
        yemek1 TEXT NOT NULL,
        yemek2 TEXT,
        yemek3 TEXT,
        yemek4 TEXT,
        yemek5 TEXT
    )
    ''')

    # Örnek kayıtlar ekle
    yemek_listeleri = [
        ('2025-05-21', 'Mercimek Çorbası', 'Tavuk Sote', 'Pilav', 'Mevsim Salata', 'Kabak Tatlısı'),
        ('2025-05-22', 'Tarhana Çorbası', 'Köfte', 'Makarna', 'Çoban Salata', 'Fırın Sütlaç'),
        ('2025-05-23', 'Ezogelin Çorbası', 'Et Sote', 'Bulgur Pilavı', 'Yeşil Salata', 'Meyve'),
    ]

    cursor.executemany('''
    INSERT INTO yemekler (tarih, yemek1, yemek2, yemek3, yemek4, yemek5)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', yemek_listeleri)

    conn.commit()
    conn.close()
    print("Veritabanı güncellendi ve örnek yemekler eklendi.")

if __name__ == "__main__":
    update_database()
