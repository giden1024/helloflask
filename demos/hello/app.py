# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import click,os
from flask import Flask, request, redirect, url_for, make_response,jsonify,session

app = Flask(__name__)


# the minimal Flask application
@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'


# bind multiple URL for one view function
@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask!</h1>'


@app.route('/newhi')
def say_helloagain():
    return '<h1>hello flask again!</h1>'


# dynamic route, URL variable default
@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name


# custom flask cli command
@app.cli.command()
def hello():
    """Just say hello."""
    click.echo('Hello, Human!')

@app.route('/helloa')
def hello_again():
    name = request.args.get('name','mymymy')
    return '<h1>hello,%s</h1>'%name

@app.route('/goback/<int:year>')
def goback(year):
    return '<h1>welcome to %d.</h1>'%(2020-year)

@app.route('/another')
def another():
    return '',302,{'Location':'https://www.bing.com'}

@app.route('/another2')
def another2():
    return redirect(url_for('hello_again'))


@app.route('/foo')
def foo():
    # data = {
    #     'name':'Grey li',
    #     'gender':'male'
    # }
    # response = make_response(json.dumps(data))
    # response.mimetype = 'application/json'
    # return response
    return jsonify(name = 'Grey li',gender = 'male')


@app.route('/set/<name>')
def foo2(name):
    response = make_response(redirect(url_for('hello_again')))
    response.set_cookie('name',name)
    return  response


@app.route('/')
@app.route('/hello2')
def hello2():
    name = request.args.get('name')
    if name is None:
        name = request.args.get('name','wuhan')
    return '<h1>Hello,%s</h1>'%name

app.secret_key = os.getenv('SECRET_KEY','DRMHZE6EPDSJKJKHJSD89_81bj-na')
@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello_again'))