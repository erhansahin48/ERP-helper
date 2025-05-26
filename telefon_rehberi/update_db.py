from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:/Users/DELL/telefon_rehberi/rehber.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Siparis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(50))
    sipno = db.Column(db.String(50))
    musteri = db.Column(db.String(100))
    termin = db.Column(db.Date)
    hafta = db.Column(db.String(10))
    artno = db.Column(db.String(50))
    ebat = db.Column(db.String(50))
    renkno = db.Column(db.String(20))
    renk = db.Column(db.String(50))
    kalan_mktar = db.Column(db.Float)
    sevk_miktar = db.Column(db.Float)
    sip_ad = db.Column(db.String(100))
    fas_cik = db.Column(db.Float)
    fas_gir = db.Column(db.Float)
    nak_cik = db.Column(db.Float)
    nak_gir = db.Column(db.Float)
    klt1 = db.Column(db.Float)
    klt2 = db.Column(db.Float)
    klt3 = db.Column(db.Float)
    etiket = db.Column(db.String(100))
    poset = db.Column(db.String(100))
    bc_ad = db.Column(db.String(100))
    mk_ad = db.Column(db.String(100))
    nakis = db.Column(db.String(100))
    baski = db.Column(db.String(100))
    koli = db.Column(db.String(100))
    koli_ici = db.Column(db.String(100))
    net_ks = db.Column(db.Float)
    adetli_net = db.Column(db.Float)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Siparis tablosu rehber.db veritabanına eklendi.")
