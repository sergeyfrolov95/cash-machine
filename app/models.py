from app import db


class Card(db.Model):

    __tablename__ = 'card'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(16), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    balance = db.Column(db.DECIMAL(12, 2), nullable=False)
    lock = db.Column(db.Boolean, nullable=False)


class Log(db.Model):

    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    date = db.Column(db.DateTime)
    details = db.Column(db.String(256))
