from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import check_password_hash
import csv
from io import StringIO
from flask import Response
import pandas as pd
from flask import send_file
import io

app = Flask(__name__)
app.secret_key = 'guvenli_bir_anahtar'  # Güçlü ve gizli tut

def get_db_connection():
    conn = sqlite3.connect('rehber.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    kisiler = conn.execute('SELECT * FROM kisiler').fetchall()
    conn.close()
    return render_template('rehber.html', rehber=kisiler)

@app.route('/login', methods=['GET', 'POST'])
def login():
    hata = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM kullanicilar WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash('Başarıyla giriş yapıldı.')
            return redirect(url_for('admin_panel'))
        else:
            hata = '❌ Kullanıcı adı veya şifre yanlış.'

    return render_template('login.html', hata=hata)

@app.route('/logout')
def logout():
    session.clear()
    flash('Başarıyla çıkış yapıldı.')
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET'])
def admin_panel():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    kisiler = conn.execute('SELECT * FROM kisiler').fetchall()
    conn.close()
    return render_template('admin.html', rehber=kisiler)

@app.route('/ekle', methods=['POST'])
def ekle():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    isim = request.form['isim']
    departman = request.form['departman']
    dahili = request.form['dahili']
    email = request.form.get('email', '')
    cep = request.form.get('cep', '')

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO kisiler (isim, departman, dahili, email, cep) VALUES (?, ?, ?, ?, ?)',
        (isim, departman, dahili, email, cep)
    )
    conn.commit()
    conn.close()

    flash('Yeni kişi başarıyla eklendi.')
    return redirect(url_for('admin_panel'))

@app.route('/guncelle', methods=['POST'])
def guncelle():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # CSV içe aktarımı kontrolü
    if 'csv_file' in request.files:
        file = request.files['csv_file']
        if file and file.filename.endswith('.csv'):
            stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
            reader = csv.DictReader(stream)
            conn = get_db_connection()
            for row in reader:
                conn.execute('''
                    INSERT INTO kisiler (isim, departman, dahili, email, cep)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row.get('isim'), row.get('departman'), row.get('dahili'), row.get('email'), row.get('cep')))
            conn.commit()
            conn.close()
            flash('CSV başarıyla içe aktarıldı.')
        else:
            flash('Lütfen geçerli bir CSV dosyası seçin.')
        return redirect(url_for('admin_panel'))
@app.route('/export_excel')
def export_excel():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    kisiler = conn.execute('SELECT * FROM kisiler').fetchall()
    conn.close()

    # Veri listesini pandas DataFrame'e çevir
    df = pd.DataFrame(kisiler, columns=kisiler[0].keys() if kisiler else [])

    # Excel dosyasını bellekte oluştur (disk yerine)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='TelefonRehberi')
    output.seek(0)

    # Excel dosyasını kullanıcıya indirilecek şekilde gönder
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        download_name='telefon_rehberi.xlsx',
        as_attachment=True
    )

    # Güncelleme işlemi
    guncelle_id = request.form.get('guncelle_id')
    if not guncelle_id:
        flash('Güncellenecek kişi seçilmedi.')
        return redirect(url_for('admin_panel'))

    isim = request.form.get(f'isim_{guncelle_id}')
    departman = request.form.get(f'departman_{guncelle_id}')
    dahili = request.form.get(f'dahili_{guncelle_id}')
    email = request.form.get(f'email_{guncelle_id}')
    cep = request.form.get(f'cep_{guncelle_id}')

    conn = get_db_connection()
    conn.execute('''
        UPDATE kisiler SET isim = ?, departman = ?, dahili = ?, email = ?, cep = ?
        WHERE id = ?
    ''', (isim, departman, dahili, email, cep, guncelle_id))
    conn.commit()
    conn.close()

    flash('Kişi bilgileri başarıyla güncellendi.')
    return redirect(url_for('admin_panel'))

@app.route('/sil/<int:id>')
def sil(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM kisiler WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash('Kişi başarıyla silindi.')
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(debug=True)
