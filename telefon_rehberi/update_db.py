import sqlite3

def add_column_resim():
    conn = sqlite3.connect('rehber.db')
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE kisiler ADD COLUMN resim TEXT;")
        print("Sütun 'resim' eklendi.")
    except sqlite3.OperationalError as e:
        if 'duplicate column name' in str(e).lower():
            print("Sütun 'resim' zaten var.")
        else:
            raise e
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_column_resim()
