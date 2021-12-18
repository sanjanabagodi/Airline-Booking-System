
#http://127.0.0.1:5000/

import configparser
import os
import re
import secrets
import psycopg2
from flask import Flask, redirect, request, render_template, url_for, session, jsonify
import sqlalchemy
from sqlalchemy import create_engine

import mysql_utils



app = Flask(__name__,
            static_url_path="/",
            static_folder="static")
'''
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres+psycopg2://postgres:foodiesss@localhost:5432/abs";
db = sqlalchemy(app);
'''


app_login = False
cfg_filename = 'app.ini'
username = ''
passw = ''

cnx = "dbname=abs user=postgres password=foodiesss host=127.0.0.1 port=5432"

#cnx = psycopg2.connect( database = 'abs', user = 'postgres', password = 'foodiesss', host = '127.0.0.1', port = '5432')
#cursor = cnx.cursor()



# error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', message=e), 404

@app.errorhandler(403)
def access_forbidden(e):
    return render_template('403.html', message=e), 403

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', message=e), 500

#creating database, tables and inserting values
#mysql_utils.create_database(cnx)
#mysql_utils.create_tables(cnx)
#mysql_utils.import_test_data(cnx)



@app.route('/')
def home():
    # first page
    if not app_login:
        return redirect(url_for('login_user'))
    else:
        return redirect(url_for('travellingagent_dashboard'))



@app.route('/login_user', methods = ['GET', 'POST'])
def login_user():
    if request.method == 'GET':
        return render_template('login_user.html')
    elif request.method == "POST":
        username = request.form.get('username')
        passw = request.form.get('passw')
        app_login = mysql_utils.login_user(cnx, username, passw)
        if app_login:
            return render_template('travellingagent_dashboard.html')
        else:
            return render_template('login_user.html', error = 'Incorrect username or password!')



@app.route('/login_agent', methods = ['GET', 'POST'])
def login_agent():
    if request.method == 'GET':
        return render_template('login_agent.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        passw = request.form.get('passw')
        app_login = mysql_utils.login_agent(cnx, username, passw)
        if app_login:
            return render_template('travellingagent_dashboard.html')
        else:
            return render_template('login_agent.html', error = 'Incorrect username or password!')



'''
@app.route('/Dashboard', methods = ['GET', 'POST'])
def travellingagent_dashboard():
    if request.method == 'GET':
        return render_template('travellingagent_dashboard.html')
'''


@app.route('/plan_my_trip', methods = ['GET', 'POST'])
def plan_my_trip():
        if request.method == 'GET':
            return render_template('plan_my_trip.html')
        elif request.method == 'POST':
            return render_template('plan_my_trip.html')
            fname = request.form.get('fname')
            mname = request.form.get('mname')
            lname = request.form.get('lname')
            dob = request.form.get('dob')
            phno = request.form.get('phno')
            gender = request.form.get('gender')
            passport_no = request.form.get('passport_no')
            ctype = request.form.get('ctype')
            source = request.form.get('source')
            dest = request.form.get('dest')
            location = request.form.get('location')

            # checking if middle name exists
            if mname == "":
                        mname = NULL
            rtn = mysql_utils.plan_my_trip(cxn, fname, mname, lname, dob, phno, gender, passport_no, stype, ctype, location, source, dest)



@app.route('/booking', methods = ['GET', 'POST'])
def booking(trip_id):
    discount = round(random.uniform(70, 200), 2)
    tax = round(random.uniform(45, 100), 2)
    price = float(random.randrange(1000, 2000, 50), 2)
    final_amt = price + tax - discount
    fare_type = "online"    #default value, can be update in booking page

    if request.method == 'GET':
        return render_template('booking.html')
    elif request.method == 'POST':
        return render_template('booking.html')



@app.route('/logout')
def logout():
    if app_login:
        return redirect(url_for('login_user'))



def is_strict_match(form: dict, rules: dict):
    try:
        for key in form.keys():
            if key not in rules:
                return False
        for key in rules.keys():
            if key not in form:
                return False
        for name, regex in rules.items():
            if re.match(regex, form[name]) is None:
                return False
        return True
    except:
        # invalid form, don't fire
        return False




if __name__ == '__main__':
    # detect config file
    '''
    if os.path.exists(cfg_filename):
        try:
            cp = configparser.RawConfigParser()
            cp.read(cfg_filename)
            db_address = cp.get("database", "address")
            db_port = int(cp.get("database", "port"))
            db_username = cp.get("database", "username")
            db_password = cp.get("database", "password")
            db_database = cp.get("database", "database")
            admin_username = cp.get("admin", "username")
            admin_password = cp.get("admin", "password")
            app_login = True
            cnx = {'host': db_address,
                   'port': db_port,
                   'user': db_username,
                   'password': db_password,
                   'database': db_database,
                   'autocommit': False,
                   'cursorclass': psycopg2.cursors.DictCursor}
        except configparser.Error:
            pass
    '''

    # generate secret key for session
    app.secret_key = secrets.token_urlsafe(16)
    app.run(host="127.0.0.1",
            port=5000,
            debug=True)
