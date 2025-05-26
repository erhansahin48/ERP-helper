import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

# Flask app tanımı (yalnızca context için)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rehber.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Siparis modelin birebir Excel'e göre uyarlanmış hali
class Siparis(db.Model):
    __tablename__ = 'siparis'
    id = db.Column(db.Integer, primary_key=True)
    KALAN_MKTAR = db.Column(db.Float)
    SEVK_MIKTAR = db.Column(db.Float)
    SIPNO = db.Column(db.String(50))
    MUSTERI = db.Column(db.String(100))
    TERMIN = db.Column(db.Date)
    HAFTA = db.Column(db.String(10))
    ARTNO = db.Column(db.String(50))
    EBAT = db.Column(db.String(50))
    RENKNO = db.Column(db.String(20))
    RENK = db.Column(db.String(50))
    GR_M2 = db.Column(db.String(20))
    BORDUR = db.Column(db.String(50))
    NAKIS = db.Column(db.String(100))
    BASKI = db.Column(db.String(100))
    SIP_AD = db.Column(db.String(100))
    FAZ_YK_AD = db.Column(db.String(100))
    ETIKET = db.Column(db.String(100))
    POSET = db.Column(db.String(100))
    POS_ICI = db.Column(db.String(100))
    KOLI = db.Column(db.String(100))
    KOLI_ICI = db.Column(db.String(100))
    NET_KS = db.Column(db.Float)
    ADETLI_NET = db.Column(db.Float)
    TOPL_NET_KOLI = db.Column(db.String(50))
    MAX_KS = db.Column(db.String(50))
    ADETLI_MAX = db.Column(db.String(50))
    FAZ_TOPL_KOLI = db.Column(db.String(50))
    NETM3 = db.Column(db.String(50))
    MAXM3 = db.Column(db.String(50))
    ORT_M3 = db.Column(db.String(50))
    DOKUMA_MKT = db.Column(db.String(50))
    BC_AD = db.Column(db.String(100))
    BG_AD = db.Column(db.String(100))
    MK_AD = db.Column(db.String(100))
    BOY_DIKIM = db.Column(db.String(50))
    EN_DIKIM = db.Column(db.String(50))
    FAS_CIK = db.Column(db.Float)
    FAS_GIR = db.Column(db.Float)
    NAK_CIK = db.Column(db.Float)
    NAK_GIR = db.Column(db.Float)
    KLT1 = db.Column(db.Float)
    KLT2 = db.Column(db.Float)
    KLT3 = db.Column(db.Float)
    ORDER_NO = db.Column(db.String(50))

# Excel dosya yolunu belirt (yeni veya mevcut)
EXCEL_PATH = "sip.örnek.xlsx"  # Dosyan burada olmalı

with app.app_context():
    df = pd.read_excel(EXCEL_PATH)

    for _, row in df.iterrows():
        siparis = Siparis(
            KALAN_MKTAR=row.get("KALAN_MKTAR"),
            SEVK_MIKTAR=row.get("SEVK_MIKTAR"),
            SIPNO=row.get("SIPNO"),
            MUSTERI=row.get("MUSTERI"),
            TERMIN=pd.to_datetime(row.get("TERMIN"), errors="coerce").date() if row.get("TERMIN") else None,
            HAFTA=row.get("HAFTA"),
            ARTNO=row.get("ARTNO"),
            EBAT=row.get("EBAT"),
            RENKNO=row.get("RENKNO"),
            RENK=row.get("RENK"),
            GR_M2=row.get("GR_M2"),
            BORDUR=row.get("BORDUR"),
            NAKIS=row.get("NAKIS"),
            BASKI=row.get("BASKI"),
            SIP_AD=row.get("SIP_AD"),
            FAZ_YK_AD=row.get("FAZ_YK_AD"),
            ETIKET=row.get("ETIKET"),
            POSET=row.get("POSET"),
            POS_ICI=row.get("POS_ICI"),
            KOLI=row.get("KOLI"),
            KOLI_ICI=row.get("KOLI_ICI"),
            NET_KS=row.get("NET_KS"),
            ADETLI_NET=row.get("ADETLI_NET"),
            TOPL_NET_KOLI=row.get("TOPL_NET_KOLI"),
            MAX_KS=row.get("MAX_KS"),
            ADETLI_MAX=row.get("ADETLI_MAX"),
            FAZ_TOPL_KOLI=row.get("FAZ_TOPL_KOLI"),
            NETM3=row.get("NETM3"),
            MAXM3=row.get("MAXM3"),
            ORT_M3=row.get("ORT_M3"),
            DOKUMA_MKT=row.get("DOKUMA_MKT"),
            BC_AD=row.get("BC_AD"),
            BG_AD=row.get("BG_AD"),
            MK_AD=row.get("MK_AD"),
            BOY_DIKIM=row.get("BOY_DIKIM"),
            EN_DIKIM=row.get("EN_DIKIM"),
            FAS_CIK=row.get("FAS_CIK"),
            FAS_GIR=row.get("FAS_GIR"),
            NAK_CIK=row.get("NAK_CIK"),
            NAK_GIR=row.get("NAK_GIR"),
            KLT1=row.get("KLT1"),
            KLT2=row.get("KLT2"),
            KLT3=row.get("KLT3"),
            ORDER_NO=row.get("ORDER_NO"),
        )
        db.session.add(siparis)

    db.session.commit()
    print(f"{len(df)} adet sipariş başarıyla eklendi.")
