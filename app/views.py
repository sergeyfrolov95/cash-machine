from datetime import datetime
from datetime import timedelta
from flask import render_template, redirect, url_for, request
import hashlib
import jwt
from jwt.exceptions import InvalidSignatureError, DecodeError, InvalidAlgorithmError

from app import app, db
from app.models import Card, Log


def jwt_encode(data):
    return jwt.encode(data, app.config['SECRET_KEY'], algorithm='HS256')


def jwt_decode(data):
    try:
        data = jwt.decode(data, app.config['SECRET_KEY'], algorithms=['HS256'])
    except (InvalidSignatureError, DecodeError, InvalidAlgorithmError) as e:
        message = 'Autorization error'
        return redirect(url_for('error', message=message))
    return data


def check_jwt_token(token):
    data = {'card': ''}
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except (InvalidSignatureError, DecodeError, InvalidAlgorithmError) as e:
        return False, data['card'], 'error'
    token_time = datetime.fromtimestamp(data['timestamp'])
    if (token_time + timedelta(minutes=2)) < datetime.now():
        return False, data['card'], 'timeout'
    else:
        return True, data['card'], 'OK'


@app.route('/',  methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        number = request.form.get('PINbox', '')
        card = db.session.query(Card.number)\
            .filter(Card.lock == False)\
            .filter(Card.number == number.replace(' ', '')).one_or_none()
        message = 'Card locked or not exists'
        data = dict(
            card=card[0] if card else card,
            attempt=0
        )
        id = jwt_encode(data)
        return redirect(url_for('pin', id=id)) \
            if card else redirect(url_for('error', message=message))
    return render_template('index.html')


@app.route('/pin', methods=['GET', 'POST'])
def pin():
    id = request.args.get('id', '')
    if not id:
        return redirect(url_for('login'))
    id = jwt_decode(id)
    if request.method == 'POST':
        password = request.form.get('PINbox', '')
        if hashlib.md5(password.encode()).hexdigest() == \
                db.session.query(Card.password).filter(Card.number == id['card']).one_or_none()[0]:
            data = dict(
                card=id['card'],
                timestamp=datetime.now().timestamp()
            )
            data = jwt_encode(data)
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
                id = jwt_encode(id)
                return redirect(url_for('pin', id=id))

    return render_template('pin.html')


@app.route('/operations', methods=['GET', 'POST'])
def operations():
    raw_token = request.args.get('id', '')
    if raw_token:
        token = check_jwt_token(raw_token)
    else:
        message = 'Authorization error, try again'
        return redirect(url_for('error', message=message))
    if not token[0]:
        message = 'Authorization timeout, try again' \
            if token[2] == 'timeout' else 'Authorization error, try again'
        return redirect(url_for('error', message=message))
    return render_template('operations.html', id=raw_token)


@app.route('/balance')
def balance():
    raw_token = request.args.get('id', '')
    if raw_token:
        token = check_jwt_token(raw_token)
    else:
        message = 'Authorization error, try again'
        return redirect(url_for('error', message=message))
    if not token[0]:
        message = 'Authorization timeout, try again' \
            if token[2] == 'timeout' else 'Authorization error, try again'
        return redirect(url_for('error', message=message))
    balance = db.session.query(Card.balance).filter(Card.number == token[1]).one_or_none()
    db.session.add(
        Log(
            card_id=db.session.query(Card.id).filter(Card.number == token[1]).one_or_none()[0],
            date=datetime.now(),
            details='Card balance request.'
            )
    )
    db.session.commit()
    message = 'Your balance for {} is {}'.format(
        datetime.now().strftime('%d.%m.%Y'),
        balance[0]
        ) if balance else 'Balance is not avaliable'

    return render_template('balance.html', balance=message, id=raw_token)


@app.route('/cash', methods=['GET', 'POST'])
def cash():
    raw_token = request.args.get('id', '')
    if raw_token:
        token = check_jwt_token(raw_token)
    else:
        message = 'Authorization error, try again'
        return redirect(url_for('error', message=message))
    if not token[0]:
        message = 'Authorization timeout, try again' \
            if token[2] == 'timeout' else 'Authorization error, try again'
        return redirect(url_for('error', message=message))

    if request.method == 'POST':
        amount = request.form.get('PINbox', '')
        if float(amount) > db.session.query(Card.balance).filter(Card.number == token[1]).one_or_none()[0]:
            message = 'Not enough money for your request'
            return redirect(url_for('error', message=message))
        else:
            subquery = db.session.query(Card.balance).filter(Card.number == token[1])
            db.session.query(Card).filter(Card.number == token[1])\
                .update({Card.balance: float(subquery.one_or_none()[0]) - float(amount)})
            db.session.add(
                Log(
                    card_id=db.session.query(Card.id).filter(Card.number == token[1]).one_or_none()[0],
                    date=datetime.now(),
                    details='Withdrawal of amount {}.'.format(amount)
                    )
            )
            db.session.commit()
            return redirect(url_for('cash_report', id=raw_token, amount=amount))

    return render_template('cash.html')


@app.route('/cash-report')
def cash_report():
    raw_token = request.args.get('id', '')
    if raw_token:
        token = check_jwt_token(raw_token)
    else:
        message = 'Authorization error, try again'
        return redirect(url_for('error', message=message))
    if not token[0]:
        message = 'Authorization timeout, try again' \
            if token[2] == 'timeout' else 'Authorization error, try again'
        return redirect(url_for('error', message=message))

    card_query = db.session.query(Card.number, Card.balance) \
        .filter(Card.number == token[1]).one_or_none()
    report = 'On your card {} withdrawed money on amount {}\
            at {}. Current balance is {}' \
            .format(
                card_query[0],
                request.args.get('amount', ''),
                datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
                card_query[1]
            )
    return render_template('cash_report.html', id=raw_token, report=report)


@app.route('/error')
def error():
    return render_template('error.html', message=request.args.get('message', 'kek'))
