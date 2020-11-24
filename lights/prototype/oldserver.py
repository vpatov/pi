#!/usr/bin/python
# coding: utf-8
from flask import Flask
import subprocess


app = Flask(__name__)

index_html="""
<html>
<link type="text/css" rel="stylesheet" href="/static/styles.css" media="screen">
<body style="font-size: 24px">
<a href="/on">on</a>
<a href="/off">off</a>
<p>
{}
</p>
</body>
</html>
"""

def run_script(on=True):
    subprocess.run('/home/vas/proj/lights/lights.sh {}'.format('on' if on else 'off'), shell=True)

@app.route('/')
def entry_point():
    return index_html.format('')

@app.route('/off')
def lights_off():
    run_script(False)
    return index_html.format('Just turned off!')

@app.route('/on')
def lights_on():
    run_script(True)
    return index_html.format('Just turned on! From Pi99 Robot Hi!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)

