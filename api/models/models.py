from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Produto(db.Model):
    __tablename__ = "PRODUTO"
    co_produto = db.Column(db.Integer, primary_key=True)
    no_produto = db.Column(db.String(200), nullable=False)
    pc_taxa_juros = db.Column(db.Numeric(10, 9), nullable=False)
    nu_minimo_meses = db.Column(db.SmallInteger, nullable=False)
    nu_maximo_meses = db.Column(db.SmallInteger, nullable=True)
    vr_minimo = db.Column(db.Numeric(18, 2), nullable=False)
    vr_maximo = db.Column(db.Numeric(18, 2), nullable=True)
