
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
        '''
        if username == 'user_user1' and passw == 'pqrs':
            return render_template('travellingagent_dashboard.html')
        elif username == 'user_user2' and passw == '3456':
            return render_template('travellingagent_dashboard.html')
        elif username != 'user_user1' or username != 'user_user2':
            return render_template('login_user.html', error = 'Username is invalid. Please enter a valid username')
        elif passw != 'pqrs' or passw != '3456':
            return render_template('login_user.html', error = 'Incorrect password.')'''



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
        if username == 'travelling_agent_alex' and passw == 'abcd':
            return render_template('travellingagent_dashboard.html')
        elif username == 'travelling_agent_julia' and passw == '1234':
            return render_template('travellingagent_dashboard.html')
        elif username != 'travelling_agent_alex' or username != 'travelling_agent_julia':
            return render_template('login_agent.html', error = 'Agent id is invalid. Please enter a valid agent id.')
        elif passw != 'abcd' or passw != '1234':
            return render_template('login_agent.html', error = 'Incorrect password.')
        '''



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
        return 'ok'



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



'''
@app.route('/searchFlight/location', methods=['GET', 'POST'])
def search_flight_by_location():
    if not app_login:
        return redirect(url_for('login_user'))
    elif request.method == 'GET':
        return render_template('searchFlightByLocation.html')
    elif request.method == 'POST':
        return render_template('searchFlightByLocation.html')

        rtn = mysql_utils.search_flight_by_location(source=request.form.get('source'),
                                                    destination=request.form.get('destination'))
        if rtn:
            head = [' '.join(w.capitalize() for w in s.split('_')) for s in rtn[0].keys()]
            if session.get('isLogin') and session.get('type') in ('login_user', 'login_agent'):
                data = [list(row.values()) + [
                    url_for('purchase_flight', airline_name=row.get('airline_name'), flight_num=row.get('flight_num'))]
                        for
                        row in rtn]
            else:
                data = [list(row.values()) + [''] for row in rtn]
            return render_template('searchFlightByLocation.html', head=head, data=data)
        else:
            return render_template('searchFlightByLocation.html',
                                   error="Your search found no result. Please modify your search.")


@app.route('/searchFlight/flightNum', methods=['GET', 'POST'])
def search_flight_by_flight_num():
    if not app_login:
        return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('searchFlightByFlightNum.html')
    elif request.method == 'POST':
        rules = {
            'flight_num': r'^\d+$',
            'date': r'^\d{4}\/\d{2}\/\d{2}$'
        }
        if not is_strict_match(request.form, rules):
            return render_template('searchFlightByFlightNum.html',
                                   error='Invalid search parameters. Please modify your search.')
        rtn = mysql_utils.search_flight_by_flight_num(cnx=cnx,
                                                      flight_num=request.form.get('flight_num'),
                                                      date=request.form.get('date'))
        if rtn:
            head = [' '.join(w.capitalize() for w in s.split('_')) for s in rtn[0].keys()]
            if session.get('isLogin'):
                data = [list(row.values()) + [
                    url_for('purchase_flight', airline_name=row.get('airline_name'), flight_num=row.get('flight_num'))]
                        for
                        row in rtn]
            else:
                data = [list(row.values()) + [''] for row in rtn]
            return render_template('searchFlightByFlightNum.html', head=head, data=data)
        else:
            return render_template('searchFlightByFlightNum.html',
                                   error="Your search found no result. Please modify your search.")


@app.route('/purchaseFlight/<airline_name>/<flight_num>', methods=['POST'])
def purchase_flight(airline_name, flight_num):
    if not app_login:
        return redirect(url_for('login'))
    elif session.get('isLogin') and session.get('type') in ('customer', 'booking_agent'):
        if session.get('type') == 'customer':
            rtn = mysql_utils.purchase_flight(cnx=cnx,
                                              customer_email=session.get('email'),
                                              airline_name=airline_name,
                                              flight_num=flight_num)
        else:  # booking_agent
            rules = {'customer_email': r'^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$'}
            if not is_strict_match(request.form, rules):
                return render_template('searchFlightByLocation.html', error="Customer email address is invalid.")
            rtn = mysql_utils.purchase_flight(cnx=cnx,
                                              customer_email=request.form.get('customer_email'),
                                              airline_name=airline_name,
                                              flight_num=flight_num,
                                              booking_agent_email=session.get('email'))
        if rtn.get('exec'):
            return render_template('searchFlightByLocation.html', success=True)
        else:
            return render_template('searchFlightByLocation.html', error=rtn.get('error'))
    else:
        return redirect(url_for('home'))


@app.route('/viewMyFlight', methods=['GET', 'POST'])
def view_my_flight():
    if not app_login:
        return redirect(url_for('login'))
    elif session.get('isLogin') and session.get('type') in ('login_user', 'login_agent'):
        if session.get('type') == 'customer':
            rtn = mysql_utils.view_my_flight_customer(email=session.get('email'),
                                                      location=request.form.get('location'),
                                                      start_date=request.form.get('start_date'),
                                                      end_date=request.form.get('end_date'))
        else:
            rtn = mysql_utils.view_my_flight_booking_agent(
                cnx=cnx,
                email=session.get('email'),
                location=request.form.get('location'),
                start_date=request.form.get('start_date'),
                end_date=request.form.get('end_date'))
        if rtn:
            head = [' '.join(w.capitalize() for w in s.split('_')) for s in rtn[0].keys()]
            data = [list(row.values()) + [''] for row in rtn]
            return render_template('viewMyFlight.html', head=head, data=data)
        else:
            return render_template('viewMyFlight.html', error='Your search found no result. Please modify your search.')
    else:
        return redirect(url_for('home'))




@app.route('/viewTopCustomers')
def view_top_customers():
    if not app_login:
        return redirect(url_for('login'))
    elif session.get('isLogin') and session.get('type') == 'booking_agent':
        rtn = mysql_utils.view_top_customers(cnx=cnx,
                                             email=session.get('email'))
        if rtn:
            return render_template('viewTopCustomers.html',
                                   commission_x=list(rtn.get('commission').keys()),
                                   commission_data=list(rtn.get('commission').values()),
                                   ticket_x=list(rtn.get('ticket').keys()),
                                   ticket_data=list(rtn.get('ticket').values()))
        else:
            return render_template('viewTopCustomers.html', error='Unable to display the top customer statistics.')
    else:
        return redirect(url_for('home'))



@app.route('/airlineStaff/viewPassengers/<airline_name>/<flight_num>')
def view_passengers(airline_name, flight_num):
    if not app_login:
        return redirect(url_for('login'))
    elif session.get('isLogin') and session.get('type') == 'airline_staff':
        rtn = mysql_utils.view_passengers(cnx=cnx,
                                          airline_staff_username=session.get('username'),
                                          airline_name=airline_name,
                                          flight_num=flight_num)
        if rtn:
            return render_template('viewPassengers.html', airline_name=airline_name, flight_num=flight_num, data=rtn)
        else:
            return render_template('viewPassengers.html', airline_name=airline_name, flight_num=flight_num,
                                   error='Either you have no permission to view this flight information or your query returned nothing.')
    else:
        return redirect(url_for('home'))


@app.route('/airlineStaff/addFlight', methods=['POST'])
def add_flight():
    if not app_login:
        return redirect(url_for('login'))
    elif session.get('isLogin') and session.get('type') == 'airline_staff':
        rules = {'departure_airport': r'^.+$',
                 'departure_time': r'^\d{3,4}\/\d{2}\/\d{2} \d{1,2}\:\d{2}$',
                 'arrival_airport': r'^.+$',
                 'arrival_time': r'^\d{3,4}\/\d{2}\/\d{2} \d{1,2}\:\d{2}$',
                 'flight_num': r'^\d+$',
                 'price': r'^[0-9|.]+$',
                 'status': r'^.+$',
                 'airplane_id': r'^\d+$'}
        if not is_strict_match(request.form, rules):
            return render_template('addFlight.html',
                                   error='Unable to add flight due to invalid form data.')
        else:
            rtn = mysql_utils.add_flight(cnx=cnx,
                                         airline_staff_username=session.get('username'),
                                         flight_num=request.form.get('flight_num'),
                                         departure_airport=request.form.get('departure_airport'),
                                         departure_time=request.form.get('departure_time'),
                                         arrival_airport=request.form.get('arrival_airport'),
                                         arrival_time=request.form.get('arrival_time'),
                                         price=request.form.get('price'),
                                         status=request.form.get('status'),
                                         airplane_id=request.form.get('airplane_id'))
            if rtn.get('exec'):
                return render_template('addFlight.html', success='You have added the flight.')
            else:
                return render_template('addFlight.html',
                                       error='Unable to add flight: %s' % rtn.get('error'))
    else:
        return redirect(url_for('home'))


@app.route('/airlineStaff/updateStatus/<airline_name>/<flight_num>', methods=['POST'])
def update_status(airline_name, flight_num):
    if not app_login:
        return redirect(url_for('login'))
    elif session.get('isLogin') and session.get('type') == 'airline_staff':
        if not request.form.get('new_status'):
            return render_template('updateStatus.html', error='New status cannot be empty.')
        rtn = mysql_utils.update_status(cnx=cnx,
                                        airline_staff_username=session.get('username'),
                                        airline_name=airline_name,
                                        flight_num=flight_num,
                                        new_status=request.form.get('new_status'))
        if rtn.get('exec'):
            return render_template('updateStatus.html', success='You have updated the flight status.')
        else:
            return render_template('updateStatus.html',
                                   error='Unable to update the flight status: %s' % rtn.get('error'))
    else:
        return redirect(url_for('home'))


@app.route('/airlineStaff/addAirplane', methods=['GET', 'POST'])
def add_airplane():
    if not app_login:
        return redirect(url_for('login'))
    elif session.get('isLogin') and session.get('type') == 'airline_staff':
        if request.method == 'GET':
            rtn_query = mysql_utils.get_airplane(cnx=cnx,
                                                 airline_staff_username=session.get('username'))
            if rtn_query:
                head = [' '.join(w.capitalize() for w in s.split('_')) for s in rtn_query[0].keys()]
                data = [list(row.values()) for row in rtn_query]
                return render_template('addAirplane.html', head=head, data=data)
            else:  # nothing returned
                return render_template('addAirplane.html', error='There is no airplane information to display.')
        elif request.method == 'POST':
            rules = {'airplane_id': r'^\d+$',
                     'seats': r'^\d+$'}
            if not is_strict_match(request.form, rules):
                return render_template('addAirplane.html', error='Unable to add airplane due to invalid form data.')
            rtn_exec = mysql_utils.add_airplane(cnx=cnx,
                                                airline_staff_username=session.get('username'),
                                                airplane_id=request.form.get('airplane_id'),
                                                seats=request.form.get('seats'))
            if rtn_exec.get('exec'):
                return render_template('addAirplane.html', success=True)
            else:
                return render_template('addAirplane.html', error='Unable to add airplane: %s' % rtn_exec.get('error'))
    else:
        return redirect(url_for('home'))


@app.route('/airlineStaff/addAirport', methods=['GET', 'POST'])
def add_airport():
    if not app_login:
        return redirect(url_for('login'))
    elif session.get('isLogin') and session.get('type') == 'airline_staff':
        if request.method == 'GET':
            rtn_query = mysql_utils.get_airport(cnx=cnx)
            if rtn_query:
                head = [' '.join(w.capitalize() for w in s.split('_')) for s in rtn_query[0].keys()]
                data = [list(row.values()) for row in rtn_query]
                return render_template('addAirport.html', head=head, data=data)
            else:  # nothing returned
                return render_template('addAirport.html', error='There is no airport information to display.')
        elif request.method == 'POST':
            rules = {'airport_name': r'^.+$',
                     'airport_city': r'^.+$'}
            if not is_strict_match(request.form, rules):
                return render_template('addAirport.html', error='Unable to add airport due to invalid form data.')
            rtn_exec = mysql_utils.add_airport(cnx=cnx,
                                               airport_name=request.form.get('airport_name'),
                                               airport_city=request.form.get('airport_city'))
            if rtn_exec.get('exec'):
                return render_template('addAirport.html', success=True)
            else:
                return render_template('addAirport.html', error='Unable to add airport: %s' % rtn_exec.get('error'))
    else:
        return redirect(url_for('home'))


@app.route('/airlineStaff/viewTopBookingAgents')
def view_top_booking_agents():
    if not app_login:
        return redirect(url_for('login'))
    elif session.get('isLogin') and session.get('type') == 'airline_staff':
        rtn = mysql_utils.view_top_booking_agents(cnx=cnx,
                                                  airline_staff_username=session.get('username'))
        if rtn.get('ticket_month'):
            htm = [' '.join(w.capitalize() for w in s.split('_')) for s in rtn.get('ticket_month')[0].keys()]
            dtm = [list(row.values()) for row in rtn.get('ticket_month')]
            hty = [' '.join(w.capitalize() for w in s.split('_')) for s in rtn.get('ticket_year')[0].keys()]
            dty = [list(row.values()) for row in rtn.get('ticket_year')]
            hc = [' '.join(w.capitalize() for w in s.split('_')) for s in rtn.get('commission')[0].keys()]
            dc = [list(row.values()) for row in rtn.get('commission')]
            return render_template('viewTopBookingAgents.html',
                                   htm=htm, dtm=dtm,
                                   hty=hty, dty=dty,
                                   hc=hc, dc=dc)
        else:
            return render_template('viewTopBookingAgents.html', error='Unable to display top booking agents data.')
    else:
        return redirect(url_for('home'))


@app.route('/airlineStaff/viewFrequentCustomer')
def view_frequent_customer():
    if not app_login:
        return redirect(url_for('login'))
    elif session.get('isLogin') and session.get('type') == 'airline_staff':
        rtn = mysql_utils.view_frequent_customer(cnx=cnx,
                                                 airline_staff_username=session.get('username'))
        if rtn:
            return render_template('viewFrequentCustomer.html', email=rtn)
        else:
            return render_template('viewFrequentCustomer.html',
                                   error='Unable to display the most frequent customer data.')
    else:
        return redirect(url_for('home'))


@app.route('/airlineStaff/viewCustomerFlightHistory', methods=['GET', 'POST'])
def view_customer_flight_history():
    if not app_login:
        return redirect(url_for('login'))
    elif session.get('isLogin') and session.get('type') == 'airline_staff':
        if request.method == 'GET':
            return render_template('viewCustomerFlightHistory.html')
        elif request.method == 'POST':
            rules = {'customer_email': r'^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$'}
            if not is_strict_match(request.form, rules):
                return render_template('viewCustomerFlightHistory.html',
                                       error='Unable to display history due to invalid email address.')
            rtn = mysql_utils.view_customer_flight_history(cnx=cnx,
                                                           airline_staff_username=session.get('username'),
                                                           customer_email=request.form.get('customer_email'))
            if rtn:
                head = [' '.join(w.capitalize() for w in s.split('_')) for s in rtn[0].keys()]
                data = [list(row.values()) for row in rtn]
                return render_template('viewCustomerFlightHistory.html', head=head, data=data)
            else:
                return render_template('viewCustomerFlightHistory.html',
                                       error='Unable to display customer flight history.')
    else:
        return redirect(url_for('home'))




@app.route('/airlineStaff/viewTopDestinations')
def view_top_destinations():
    if not app_login:
        return redirect(url_for('login'))
    elif session.get('isLogin') and session.get('type') == 'airline_staff':
        rtn = mysql_utils.view_top_destinations(cnx=cnx,
                                                airline_staff_username=session.get('username'))
        if rtn.get('month'):
            return render_template('viewTopDestinations.html', month=rtn.get('month'), year=rtn.get('year'))
        else:
            return render_template('viewTopDestinations.html', error='Unable to display top destinations data.')
    else:
        return redirect(url_for('home'))


# general api
@app.route('/getAllAirlines', methods=['POST'])
def get_all_airlines():
    if app_login:
        return jsonify(mysql_utils.get_all_airlines(cnx=cnx))
    else:
        return jsonify([])


@app.route('/getAllCitiesAndAirports', methods=['POST'])
def get_all_cities_and_airports():
    if app_login:
        return jsonify(mysql_utils.get_all_cities_and_airports(cnx=cnx))
    else:
        return jsonify([])



@app.route('/getAllAirports', methods=['POST'])
def get_all_airports():
    if app_login and session.get('isLogin') and session.get('type') == 'airline_staff':
        return jsonify(mysql_utils.get_all_airports(cnx=cnx))
    else:
        return jsonify([])


@app.route('/getAllAirplaneId', methods=['POST'])
def get_all_airplane_id():
    if app_login and session.get('isLogin') and session.get('type') == 'airline_staff':
        return jsonify(mysql_utils.get_all_airplane_id(cnx=cnx))
    else:
        return jsonify([])
'''


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
