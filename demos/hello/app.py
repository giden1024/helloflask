# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import click,os
from flask import Flask, request, redirect, url_for, make_response, jsonify, session, abort
from urllib.parse import urlparse,urljoin


app = Flask(__name__)


# the minimal Flask application
# @app.route('/')
# def index():
#     return '<h1>Hello, World!</h1>'


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
    response = make_response(redirect(url_for('hello2')))
    response.set_cookie('name',name)
    return  response



@app.route('/')
@app.route('/hello2')
def hello2():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name','wuhan')
        response = '<h1>Hello,%s</h1>'%name
    if 'logged_in' in session:
        response +='[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response

app.secret_key = os.getenv('SECRET_KEY','DRMHZE6EPDSJKJKHJSD89_81bj-na')
@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello2'))


@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page'


@app.route('/logout')
def logout():
    if 'logged_id' in session:
        session['logged_in'] = False
    return redirect(url_for('hello2'))


def redirect_back(default = 'hello2',**kwargs):
    for target in request.args.get('next'),request.referrer:
        if target:
            return redirect(target)
    return redirect(default,**kwargs)


@app.route('/do_something')
def do_something():
    # return redirect(request.referrer or url_for('hello2'))
    # print(request.args.get('next'))
    # return redirect(request.args.get('next',url_for('hello2')))
    return redirect_back()

@app.route('/foo1')
def foo1():
    return '<h1>Foo page<a href="%s">back</a></h1>'%url_for('do_something',next = request.full_path)

@app.route('/bar')
def bar():
    return '<h1>Bar page<a href="%s">bar</a></h1>'%url_for('do_something',next = request.full_path)
