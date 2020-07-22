import os

import flask
from flask import Flask, redirect, url_for, request, render_template, jsonify
from pymongo import MongoClient

import acp_times
import arrow

import logging
import config

app = Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY


#client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
client = MongoClient('db',27017)
db = client.tododb #connect to database
db.tododb.delete_many({}) #clear last database

@app.route('/')
@app.route('/index')
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("404 Error: Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return render_template('404.html'), 404

#new implementation
@app.route('/display', methods=['POST'])
def todo():
    _items = db.tododb.find()
    items = [item for item in _items]

    if items is []:
        return render_template('empty.html')
    else:
        return render_template('todo.html', items=items)

@app.route('/new', methods=['POST'])
def new():
    openlist = []
    _open = request.form.getlist("open")
    for o in _open:
        if str(o) != "":
            openlist.append(str(o))

    closelist = []
    close = request.form.getlist("close")
    for c in close:
        if str(c) != "":
            closelist.append(str(c))

    for i in range(len(openlist)):
        time = {
        'otime': openlist[i],
        'ctime': closelist[i]
        }
        db.tododb.insert_one(time)

    _items = db.tododb.find()
    items = [item for item in _items]
    app.logger.debug("CONTENTS: "+str(items))
    if items != []:
        return redirect(url_for('index'))
    else:
        return render_template('404.html')
#proj4 implementation
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")

    km = request.args.get('km', 999, type=float)
    date = request.args.get('date', 999, type=str)
    time = request.args.get('time', 999,type=str)
    distance = request.args.get('distance', 999,type=float)

    #format date
    date_format = str(date) + ' ' + str(time) + ':00'
    arrow_time = arrow.get(date_format, 'YYYY-MM-DD HH:mm:ss')

    open_time = acp_times.open_time(km, distance, arrow_time.isoformat())
    close_time = acp_times.close_time(km, distance, arrow_time.isoformat())
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
