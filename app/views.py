from app import app, db
from app.models import Card, Log
from flask import render_template


@app.route('/')
def login():
    q = db.session.query(Card).all()
    print(q)
    return render_template('index.html')


@app.route('/pin')
def pin():
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
    return None
