#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, request, redirect
import logging
import sys
import warnings

app = Flask(__name__) 
app.debug = True
logger = logging.getLogger(__name__)

@app.route('/') 
def hello(): 
    logger.info("hello")
    return "Hello World."
    
@app.route('/form')
def form():
    return '<http><body><form method="POST" action="/first"><input type="text" name="foo"/><input type="submit"></form></body></http>'

@app.route('/first', methods=['POST'])
def first():
    """Trigger with:
    $ http -f --follow POST http://0.0.0.0:5000/first foo="bar"
    """
    foo = request.form['foo']
    logger.info("foo: %s", foo)
    return redirect("/second", code=307)

@app.route('/second', methods=['POST'])
def second():
    foo = request.form['foo']
    logger.info("foo: %s", foo)
    return redirect('/')

@app.before_first_request
def init_logger(verbosity=3, stream=sys.stdout):
    '''Initialize logger and warnings according to verbosity argument.
    Verbosity levels of 0-3 supported.'''
    is_not_debug = verbosity <= 2
    level = [logging.ERROR, logging.WARNING, logging.INFO][verbosity] if is_not_debug else logging.DEBUG
    format = '%(message)s' if is_not_debug else '%(asctime)s %(levelname)-8s %(name)s %(module)s.py:%(funcName)s():%(lineno)d %(message)s'
    logging.basicConfig(level=level, format=format, stream=stream)
    if is_not_debug: warnings.filterwarnings('ignore')