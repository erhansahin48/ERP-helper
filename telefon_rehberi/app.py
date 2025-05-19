from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import check_password_hash
import csv
from io import StringIO
from flask import Response
import pandas as pd
from flask import send_file
from io import BytesIO
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
import openpyxl
from datetime import datetime
from flask import g
import sqlite3
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
    return render_template_tarihli('base.html', rehber=kisiler)


def tarih_formatla(tarih):
    if isinstance(tarih, datetime):
        return tarih.strftime('%d.%m.%Y')
    elif isinstance(tarih, str):
        try:
            dt = datetime.fromisoformat(tarih)  # '2024-05-19' gibi ise
            return dt.strftime('%d.%m.%Y')
        except:
            return tarih
    return tarih

def recursive_format(value):
    if isinstance(value, list):
        return [recursive_format(v) for v in value]
    elif isinstance(value, dict):
        return {k: recursive_format(v) for k, v in value.items()}
    else:
        return tarih_formatla(value)
        
def render_template_tarihli(template_name, **context):
    formatted_context = {k: recursive_format(v) for k, v in context.items()}
    return render_template(template_name, **formatted_context)




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
            return redirect(url_for('admin_rehber'))
        else:
            hata = '❌ Kullanıcı adı veya şifre yanlış.'

    return render_template('login.html', hata=hata)

@app.route('/logout')
def logout():
    session.clear()
    flash('Başarıyla çıkış yapıldı.')
    return redirect(url_for('login'))

@app.route('/admin_rehber', methods=['GET'])
def admin_rehber():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    kisiler = conn.execute('SELECT * FROM kisiler').fetchall()
    conn.close()
    return render_template_tarihli('panel_template/rehber_edit.html', rehber=kisiler)


@app.route('/ekle', methods=['POST'])
def ekle():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if 'csv_file' in request.files:
        return redirect(url_for('ekle_csv'))  # Yeni route’a yönlendir

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
    return redirect(url_for('admin_rehber'))


    # CSV içe aktarımı kontrolü
@app.route('/ekle_csv', methods=['POST'])
def ekle_csv():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    file = request.files.get('csv_file')
    if file and file.filename.endswith('.csv'):
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)
        conn = get_db_connection()
        for row in reader:
            conn.execute('''INSERT INTO kisiler (isim, departman, dahili, email, cep)
                            VALUES (?, ?, ?, ?, ?)''',
                         (row.get('isim'), row.get('departman'), row.get('dahili'), row.get('email'), row.get('cep')))
        conn.commit()
        conn.close()
        flash('CSV başarıyla içe aktarıldı.')
    else:
        flash('Lütfen geçerli bir CSV dosyası seçin.')

    return redirect(url_for('admin_rehber'))


@app.route('/guncelle', methods=['POST'])
def guncelle():
    # Güncelleme kodlarınız burada
    guncelle_id = request.form.get('guncelle_id')
    if not guncelle_id:
        flash('Güncellenecek kişi seçilmedi.')
        return redirect(url_for('admin_rehber'))

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
    return redirect(url_for('admin_rehber'))

@app.route('/export_excel')
def export_excel():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    kisiler = conn.execute('SELECT isim, departman, dahili, email, cep FROM kisiler').fetchall()
    conn.close()

    kisiler_liste = [dict(kisi) for kisi in kisiler]

    df = pd.DataFrame(kisiler_liste, columns=['isim', 'departman', 'dahili', 'email', 'cep'])
    df.columns = ['İsim Soyisim', 'Departman', 'Dahili No', 'E-Posta', 'Cep Telefonu']

    # Yeni Excel dosyası
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Rehber'

    # Veri çerçeveye yaz
    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
        for c_idx, value in enumerate(row, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=value)

            # Tüm hücreler ortalı
            cell.alignment = Alignment(horizontal='center', vertical='center')

            # Başlık satırına kalın yazı ve arka plan
            if r_idx == 1:
                cell.font = Font(bold=True)

            # Kenarlık ekle
            cell.border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )

    # Sütunları otomatik genişlet
    for col in ws.columns:
        max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_length + 2

    # Excel dosyasını belleğe yaz
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        download_name="telefon_rehberi.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@app.route('/sil/<int:id>')
def sil(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM kisiler WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash('Kişi başarıyla silindi.')
    return redirect(url_for('admin_rehber'))



@app.route('/rehber')
def rehber():
    conn = get_db_connection()
    kisiler = conn.execute('SELECT * FROM kisiler').fetchall()
    conn.close()
    return render_template_tarihli('rehber.html', rehber=kisiler)

@app.route('/admin/duyurular', methods=['GET', 'POST'])
def admin_duyurular():
    db = get_db_connection()

    # POST: Yeni duyuru ekleme
    if request.method == 'POST':
        baslik = request.form.get('baslik')
        icerik = request.form.get('icerik')
        tarih = request.form.get('tarih')  # opsiyonel, yoksa bugünün tarihi atanabilir

        if not baslik or not icerik:
            flash("Başlık ve içerik zorunludur.")
            return redirect(url_for('admin_duyurular'))

        if not tarih:
            from datetime import datetime
            tarih = datetime.now().strftime('%Y-%m-%d')

        db.execute(
            "INSERT INTO duyurular (baslik, icerik, tarih) VALUES (?, ?, ?)",
            (baslik, icerik, tarih)
        )
        db.commit()
        db.close()
        flash("Duyuru başarıyla eklendi.")
        return redirect(url_for('admin_duyurular'))

    # GET: Listeleme + filtreleme
    tarih_filter = request.args.get('tarih_filter')
    siralama = request.args.get('siralama', 'desc')

    query = "SELECT * FROM duyurular"
    params = []

    if tarih_filter:
        query += " WHERE tarih >= ?"
        params.append(tarih_filter)

    query += f" ORDER BY tarih {siralama.upper()}"

    duyurular = db.execute(query, params).fetchall()
    db.close()

    return render_template_tarihli('panel_template/duyuru_edit.html', duyurular=duyurular, tarih_filter=tarih_filter, siralama=siralama)

@app.route('/admin/duyuru_sil/<int:id>', methods=['GET'])
def admin_duyuru_sil(id):
    db = get_db_connection()
    db.execute("DELETE FROM duyurular WHERE id = ?", (id,))
    db.commit()
    db.close()
    flash("Duyuru başarıyla silindi.")
    return redirect(url_for('admin_duyurular'))


@app.route('/duyurular')
def duyurular():
    conn = get_db_connection()
    duyurular = conn.execute('SELECT * FROM duyurular ORDER BY id DESC').fetchall()
    conn.close()
    return render_template_tarihli('duyurular.html', duyurular=duyurular)


# Kullanıcı için yemek listesi sayfası (sadece görüntüleme)
@app.route('/yemek-listesi')
def yemek_listesi():
    conn = get_db_connection()
    yemekler = conn.execute('SELECT * FROM yemekler ORDER BY tarih').fetchall()
    conn.close()
    return render_template_tarihli('yemek_listesi.html', yemekler=yemekler)

# Admin için yemek listesi sayfası (düzenleme yapacak)
@app.route('/admin/yemek-listesi')
def admin_yemek_listesi():
    conn = get_db_connection()
    yemekler = conn.execute('SELECT * FROM yemekler ORDER BY tarih').fetchall()
    conn.close()
    return render_template_tarihli('panel_template/yemek_edit.html', yemekler=yemekler)

# Admin - yemek ekleme
@app.route('/admin/yemek-ekle', methods=['POST'])
def admin_yemek_ekle():
    tarih = request.form['tarih']
    menu = request.form['menu']
    conn = get_db_connection()
    conn.execute('INSERT INTO yemekler (tarih, menu) VALUES (?, ?)', (tarih, menu))
    conn.commit()
    conn.close()
    flash('Yemek eklendi.')
    return redirect(url_for('admin_yemek_listesi'))

# Admin - yemek güncelleme
@app.route('/admin/yemek-guncelle', methods=['POST'])
def admin_yemek_guncelle():
    yemek_id = request.form['guncelle_id']
    tarih = request.form[f'tarih_{yemek_id}']
    menu = request.form[f'menu_{yemek_id}']
    conn = get_db_connection()
    conn.execute('UPDATE yemekler SET tarih = ?, menu = ? WHERE id = ?', (tarih, menu, yemek_id))
    conn.commit()
    conn.close()
    flash('Yemek güncellendi.')
    return redirect(url_for('admin_yemek_listesi'))

# Admin - yemek silme
@app.route('/admin/yemek-sil/<int:yemek_id>')
def admin_yemek_sil(yemek_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM yemekler WHERE id = ?', (yemek_id,))
    conn.commit()
    conn.close()
    flash('Yemek silindi.')
    return redirect(url_for('admin_yemek_listesi'))

# Admin - CSV import
@app.route('/admin/yemek-import', methods=['POST'])
def admin_yemek_import():
    file = request.files.get('csv_file')
    if not file:
        flash('Dosya seçilmedi.')
        return redirect(url_for('admin_yemek_listesi'))

    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    conn = get_db_connection()
    conn.execute('DELETE FROM yemekler')  # Eski veriyi temizler
    for row in csv_input:
        if len(row) >= 2:
            tarih, menu = row[0], row[1]
            conn.execute('INSERT INTO yemekler (tarih, menu) VALUES (?, ?)', (tarih, menu))
    conn.commit()
    conn.close()
    flash('CSV başarıyla içe aktarıldı.')
    return redirect(url_for('admin_yemek_listesi'))

# Admin - CSV export
@app.route('/admin/yemek-export')
def admin_yemek_export():
    conn = get_db_connection()
    yemekler = conn.execute('SELECT tarih, menu FROM yemekler ORDER BY tarih').fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['tarih', 'menu'])
    for yemek in yemekler:
        writer.writerow([yemek['tarih'], yemek['menu']])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='yemek_listesi.csv'
    )



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
