import sqlite3

def add_tarih_column_to_duyurular():
    conn = sqlite3.connect('rehber.db')
    c = conn.cursor()

    try:
        # duyurular tablosuna tarih sütunu ekle (eğer yoksa)
        c.execute("ALTER TABLE duyurular ADD COLUMN tarih TEXT")
        print("`tarih` sütunu başarıyla eklendi.")
    except sqlite3.OperationalError as e:
        # Eğer sütun zaten varsa hata alır, bunu yoksay
        if "duplicate column name" in str(e).lower():
            print("`tarih` sütunu zaten mevcut.")
        else:
            print("Beklenmedik hata:", e)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_tarih_column_to_duyurular()
