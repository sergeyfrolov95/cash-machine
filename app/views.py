from app import app
from flask import render_template


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/pin')
def pin():
    return None


@app.route('/operations')
def operations():
    return None


@app.route('/balance')
def balance():
    return None


@app.route('/cash')
def cash():
    return None


@app.route('/error')
def error():
    return None
