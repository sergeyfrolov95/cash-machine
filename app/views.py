from datetime import datetime
from flask import render_template, redirect, url_for, request
import hashlib
import jwt

from app import app, db
from app.models import Card, Log


@app.route('/',  methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        number = request.form.get('PINbox', '')
        card = db.session.query(Card.number)\
            .filter(Card.lock == False)\
            .filter(Card.number == number.replace(' ', '')).one_or_none()
        message = 'Card locked or not exists'
        data = dict(
            card=card[0],
            attempt=0
        )
        id = jwt.encode(data, app.config['SECRET_KEY'], algorithm='HS256')
        return redirect(url_for('pin', id=id)) \
            if card else redirect(url_for('error', message=message))
    return render_template('index.html')


@app.route('/pin', methods=['GET', 'POST'])
def pin():
    id = request.args.get('id', '')
    if not id:
        return redirect(url_for('login'))
    id = jwt.decode(id, app.config['SECRET_KEY'], algorithms=['HS256'])
    if request.method == 'POST':
        password = request.form.get('PINbox', '')
        if hashlib.md5(password.encode()).hexdigest() == \
                db.session.query(Card.password).filter(Card.number == id['card']).one_or_none()[0]:
            data = ''
            # new jwt token here in data
            return redirect(url_for('operations', id=data))
        else:
            id['attempt'] += 1
            if id['attempt'] >= 3:
                db.session.query(Card).filter(Card.number == id['card'])\
                    .update({Card.lock: True})
                db.session.add(
                    Log(
                        card_id=db.session.query(Card.id).filter(Card.number == id['card']).one_or_none()[0],
                        date=datetime.now(),
                        details='Card was blocked.'
                        )
                )
                db.session.commit()
                message = 'Too many attempts, card blocked!'
                return redirect(url_for('error', message=message))
            else:
                id = jwt.encode(id, app.config['SECRET_KEY'], algorithm='HS256')
                return redirect(url_for('pin', id=id))

    return render_template('pin.html')


@app.route('/operations')
def operations():
    return render_template('operations.html')


@app.route('/balance')
def balance():
    return None


@app.route('/cash')
def cash():
    return render_template('cash.html')


@app.route('/error')
def error():
    return request.args.get('message', 'kek')
