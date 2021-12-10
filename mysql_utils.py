import logging

import psycopg2

from colored_logger import ColoredLogger

# run when being imported as a module
# initiate logger
# for debug
logging.setLoggerClass(ColoredLogger)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



# setup functions
# implemented already, don't modify
'''
def create_database(cnx):
    error = None
    cnx = psycopg2.connect(cnx)
    cursor = cnx.cursor()
    try:
        cursor.execute("drop database if exists abs")
        cursor.execute("create database abs")
        cnx.commit()
    except Exception as ex:
        logger.error(str(ex))
        error = str(ex)
    return error


def create_tables(cnx):
    errors = []
    cnx = psycopg2.connect(cnx)
    cursor = cnx.cursor()
    with open('create_tables.sql', 'r') as fs:
        sql_commands = fs.read().split(';')
        for cmd in sql_commands:
            if cmd:
                try:
                    cursor.execute(cmd)
                except Exception as ex:
                    logger.error(str(ex))
                    errors.append(str(ex))
    cnx.commit()
    return errors


def import_test_data():
    try:
        errors = []
        cnx = psycopg2.connect(cnx)
        cursor = cnx.cursor()
        with open('import_test_data.sql', 'r') as fs:
            sql_commands = fs.read().split(';')
            for cmd in sql_commands:
                cmd = cmd.strip()
                if cmd:
                    try:
                        cursor.execute(cmd)
                    except Exception as ex:
                        logger.error(str(ex))
                        errors.append(str(ex))
        cnx.commit()
        logger.info('test data imported')
        return errors
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return [str(ex)]
'''

# helper function
def _str_datetime(val):
    return val.strftime('%Y') + '/' + val.strftime('%m') + '/' + val.strftime(
        '%d') + ' ' + val.strftime('%H') + ':' + val.strftime('%M') + ':' + val.strftime('%S')


'''
# login functions
# exec means whether sql executed successfully, if not, error means error message from sql
# login means whether user validation passed
def login_customer(cnx, email, password):
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("select count(distinct email) as number from customer where email = %s and password = %s",
                       (email, password))
        u = cursor.fetchall()[0]['number']
        if u > 0:
            cursor.execute("select name from customer where email = %s", (email,))
            name = cursor.fetchall()[0]['name']
            return {
                'login': True,
                'email': email,
                'name': name
            }
        elif u == 0:
            return {
                'login': False
            }
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return {
            'login': False
        }
    finally:
        cursor.close()
        cnx.close()
'''



def login_user(cnx, username, passw):
    try:
        cnx = psycopg2.connect(cnx)
        cursor = cnx.cursor()
        cursor.execute("select count(*) from login_user where username = %s and passw = %s", (username, passw))
        u = cursor.fetchone()[0]
        if u > 0:
            return True
        elif u == 0:
            return False
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return False
    


def login_agent(cnx, username, passw):
    try:
        cnx = psycopg2.connect(cnx)
        cursor = cnx.cursor()
        cursor.execute("select * from login_agent where username = %s and passw = %s", (username, passw))
        u = cursor.fetchone()[0]
        if u > 0:
            return True
        elif u == 0:
            return False
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return False
    




'''
# helper function
# Additional functions for some of the following functions
def _all_cities(cursor, mtplx_cnx):
    try:
        cursor = mtplx_cnx.cursor()
        cursor.execute("select distinct city from airport")
        return [name['city'] for name in cursor.fetchall()]
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return []
    finally:
        cursor.close()


# return empty list if nothing is found or error occurred
# normally return list of dict
def search_flight_by_location(cursor, source, destination):
    try:
        command = "select * from flight where and %s between date_sub(departure_time, INTERVAL 1 DAY) and arrival_time "
        if source in _all_cities(cursor):
            command += "and departure_airport in (select airport_name from airport where airport_city = %s) "
        else:
            command += "and departure_airport = %s "
        if destination in _all_cities(cursor):
            command += "and arrival_airport in (select airport_name from airport where airport_city = %s)"
        else:
            command += "and arrival_airport = %s"
        cursor.execute(command, (date, source, destination))
        result = []
        dic = cursor.fetchone()
        while dic is not None:
            dic['departure_time'] = _str_datetime(dic['departure_time'])
            dic['arrival_time'] = _str_datetime(dic['arrival_time'])
            dic['price'] = int(dic['price'])
            result.append(dic)
            dic = cursor.fetchone()
        return result
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return str(ex)
    finally:
        cursor.close()
        cnx.close()


def search_flight_by_flight_num(cursor, flight_num, date):
    try:
        cursor.execute(
            "select * from flight where flight_num = %s and %s between date_sub(departure_time,interval 1 day) and arrival_time",
            (flight_num, date))
        result = []
        dic = cursor.fetchone()
        while dic is not None:
            dic['departure_time'] = _str_datetime(dic['departure_time'])
            dic['arrival_time'] = _str_datetime(dic['arrival_time'])
            dic['price'] = int(dic['price'])
            result.append(dic)
            dic = cursor.fetchone()
        return result
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return []
    finally:
        cursor.close()
        cnx.close()




# helper function
def _generate_ticket(cursor, mtplx_cnx, ticket_id, airline, flight_number):
    try:
        check = _check_airplane_full(mtplx_cnx, flight_number, airline)
        cursor = mtplx_cnx.cursor()
        if check == 'full':
            return 'full'
        elif check == 'available':
            cursor.execute("insert into ticket values (%s,%s,%s)", (ticket_id, airline, flight_number))
            mtplx_cnx.commit()
            return 'successfully inserted'
        else:
            return check
    except psycopg2.Error as ex:
        logger.error(str(ex))
        mtplx_cnx.rollback()
        return str(ex)
    finally:
        cursor.close()


def purchase_flight(cursor, customer_email, airline_name, flight_num, booking_agent_email=None):
    try:
        cursor.execute("select max(ticket_id) as max from ticket")
        max_ticket_id = cursor.fetchall()
        if len(max_ticket_id) > 0 and max_ticket_id[0]['max'] != None:
            ticket_id = max_ticket_id[0]['max'] + 1
        else:
            ticket_id = 1
        ticket = _generate_ticket(cnx, ticket_id, airline_name, flight_num)
        if ticket == 'successfully inserted':
            if not booking_agent_email:
                cursor = cnx.cursor()
                cursor.execute("insert into purchases values(%s,%s,null,current_date)", (ticket_id, customer_email))
                cnx.commit()
                return {'exec': True}
            else:
                cursor = cnx.cursor()
                cursor.execute("select booking_agent_id from booking_agent where email = %s", (booking_agent_email,))
                dic = cursor.fetchall()
                if len(dic) > 0:
                    booking_agent_id = dic[0]['booking_agent_id']
                else:
                    return {'exec': False,
                            'error': 'no such booking agent'}
                cursor.execute("insert into purchases values(%s,%s,%s,current_date)",
                               (ticket_id, customer_email, booking_agent_id))
                cnx.commit()
                return {'exec': True}
        elif ticket == 'full':
            return {'exec': False,
                    'error': 'this flight is full'}
        else:
            return {'exec': False,
                    'error': ticket}
    except psycopg2.Error as ex:
        logger.error(str(ex))
        cnx.rollback()
        return {'exec': False,
                'error': str(ex)}
    finally:
        cursor.close()
        cnx.close()



def view_passengers(cnx, airline_staff_username, airline_name, flight_num):
    # must check if the airline really has permission to view passenger
    # if airline_staff_username --> airline_name doesn't match the airline_name, then return empty list
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("select airline_name from airline_staff where username = %s", (airline_staff_username,))
        outcome = cursor.fetchall()
        if len(outcome) > 0:
            staff_airline = outcome[0]['airline_name']
        else:
            return []
        if airline_name != staff_airline:
            return []
        cursor.execute(
            "select customer_email from purchases natural join ticket where flight_num = %s and airline_name = %s",
            (flight_num, airline_name))
        result = []
        dic = cursor.fetchone()
        while dic is not None:
            result.append(dic['customer_email'])
            dic = cursor.fetchone()
        return result
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return []
    finally:
        cursor.close()
        cnx.close()


def add_flight(cnx, airline_staff_username, flight_num, departure_airport, departure_time, arrival_airport,
               arrival_time, price,
               status, airplane_id):
    # the airline_name should be obtained from airline_staff_username
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("select airline_name from airline_staff where username = %s", (airline_staff_username,))
        list_of_dic = cursor.fetchall()
        if len(list_of_dic) > 0:
            staff_airline = list_of_dic[0]['airline_name']
        else:
            return {'exec': False,
                    'error': "the username doesn't exist"}
        cursor.execute("insert into flight values (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
            staff_airline, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status,
            airplane_id))
        cnx.commit()
        return {'exec': True}
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return str(ex)
    finally:
        cursor.close()
        cnx.close()


def update_status(cnx, airline_staff_username, airline_name, flight_num, new_status):
    # must check if the airline really has permission to view passenger
    # if airline_staff_username --> airline_name doesn't match the airline_name, then return exec=False
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("select airline_name from airline_staff where username = %s", (airline_staff_username,))
        outcome = cursor.fetchall()
        if len(outcome) > 0:
            staff_airline = outcome[0]['airline_name']
        else:
            return {'exec': False,
                    'error': 'no permission oops'}
        if staff_airline != airline_name:
            return {'exec': False,
                    'error': 'no permission oops'}
        else:
            cursor.execute("update flight set status = %s where airline_name = %s and flight_num = %s",
                           (new_status, airline_name, flight_num))
            cnx.commit()
            return {'exec': True}
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return str(ex)
    finally:
        cursor.close()
        cnx.close()


def get_airplane(cnx, company_id):
    # get the airplanes info of a particular company
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("select * from airplane where company_id = %s", (company_id))
        list_of_dic = cursor.fetchall()
        if list_of_dic:
            return list_of_dic
        else:
            return []
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return {'exec': False, 'error': str(ex)}
    finally:
        cursor.close()
        cnx.close()


def add_airplane(cnx, airplane_no, aircraft_type, seating_capacity, company_id):
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("insert into airplane values (%s,%s,%d,%s)", (airplane_no, aircraft_type, seating_capacity, company_id))
        cnx.commit()
        return {'exec': True}
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return {'exec': False, 'error': str(ex)}
    finally:
        cursor.close()
        cnx.close()


def get_airport(cnx):
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("select * from airport")
        return cursor.fetchall()
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return {}
    finally:
        cursor.close()
        cnx.close()


def add_airport(cnx, airport_code, airport_name, city, country, zipp):
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("insert into airport values (%s,%s,%s,%s,%d)", (airport_code, airport_name, city, country, zipp))
        cnx.commit()
        return {'exec': True}
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return {'exec': False, 'error': str(ex)}
    finally:
        cursor.close()
        cnx.close()


def view_top_booking_agents(cnx, airline_staff_username):
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("select airline_name from airline_staff where username = %s", (airline_staff_username,))
        list_of_dic = cursor.fetchall()
        if list_of_dic:
            staff_airline = list_of_dic[0]['airline_name']
        else:
            logger.error("username doesn't exist")
            return {}
        cursor.execute(
            "select email,count(ticket_id) as ticket from booking_agent natural join purchases natural join ticket natural join flight where purchase_date >= date_sub(CURRENT_DATE,interval 1 year) and airline_name = %s group by email order by ticket DESC",
            (staff_airline,))
        outcome1 = cursor.fetchall()
        if outcome1 and len(outcome1) > 5:
            outcome1 = outcome1[0:5]
        cursor.execute(
            "select email,count(ticket_id) as ticket from booking_agent natural join purchases natural join ticket natural join flight where purchase_date >= date_sub(CURRENT_DATE,interval 1 month) and airline_name = %s group by email order by ticket DESC",
            (staff_airline,))
        outcome2 = cursor.fetchall()
        if outcome2 and len(outcome2) > 5:
            outcome2 = outcome2[0:5]
        cursor.execute(
            "select email,sum(price)/10 as commission from booking_agent natural join purchases natural join ticket natural join flight where purchase_date >= date_sub(CURRENT_DATE,interval 1 year) and airline_name = %s group by email AND booking_agent_id order by commission DESC",
            (staff_airline,))
        outcome3 = cursor.fetchall()
        if outcome3 and len(outcome3) > 5:
            outcome3 = outcome3[0:5]
        return {'ticket_year': outcome1, 'ticket_month': outcome2, 'commission': outcome3}
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return {}
    finally:
        cursor.close()
        cnx.close()


def view_frequent_customer(cnx, airline_staff_username):
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("select airline_name from airline_staff where username = %s", (airline_staff_username,))
        list_of_dic = cursor.fetchall()
        if list_of_dic:
            staff_airline = list_of_dic[0]['airline_name']
        else:
            return []
        cursor.execute(
            "select email from customer where (select count(distinct ticket_id) from purchases natural join ticket natural join flight where customer_email = email and airline_name = %s) >= all (select count(distinct ticket_id) from purchases natural join ticket natural join flight where airline_name = %s group by customer_email)",
            (staff_airline, staff_airline))
        dic = cursor.fetchone()
        result = []
        while dic is not None:
            result.append(dic['email'])
            dic = cursor.fetchone()
        return result
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return []
    finally:
        cursor.close()
        cnx.close()


def view_customer_flight_history(cnx, airline_staff_username, customer_email):
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("select airline_name from airline_staff where username = %s", (airline_staff_username,))
        list_of_dic = cursor.fetchall()
        if list_of_dic:
            staff_airline = list_of_dic[0]['airline_name']
        else:
            return []
        cursor.execute(
            "select airline_name,flight_num from flight natural join ticket natural join purchases where customer_email = %s and airline_name = %s",
            (customer_email, staff_airline))
        dic = cursor.fetchone()
        result = []
        while dic != None:
            dic['flight_num'] = int(dic['flight_num'])
            result.append(dic)
            dic = cursor.fetchone()
        return result
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return []
    finally:
        cursor.close()
        cnx.close()



def get_all_airports(cnx):
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("select * airport_name from airport")
        dic = cursor.fetchone()
        result = []
        while dic is not None:
            result.append(dic['airport_name'])
            dic = cursor.fetchone()
        return result
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return []
    finally:
        cursor.close()
        cnx.close()


# general api
# normally returns empty list if error occurred
def get_all_airlines(cnx):
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("select * company_name from airline_company")
        dic = cursor.fetchone()
        result = []
        while dic is not None:
            result.append(dic['company_name'])
            dic = cursor.fetchone()
        return result
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return str(ex)
    finally:
        cursor.close()
        cnx.close()


def get_all_cities_and_airports(cnx):
    try:
        mtplx_cnx = psycopg2.connect(cnx)
        return _all_cities(mtplx_cnx) + get_all_airports(cnx)
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return []
    finally:
        mtplx_cnx.close()


def get_all_airports(cnx):
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("select * airport_name from airport")
        dic = cursor.fetchone()
        result = []
        while dic is not None:
            result.append(dic['airport_name'])
            dic = cursor.fetchone()
        return result
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return []
    finally:
        cursor.close()
        cnx.close()


def get_all_airplane_id(cnx):
    try:
        cnx = psycopg2.connect(**cnx)
        cursor = cnx.cursor()
        cursor.execute("select * airplane_no from airplane")
        dic = cursor.fetchone()
        result = []
        while dic is not None:
            result.append(dic['airplane_no'])
            dic = cursor.fetchone()
        return result
    except psycopg2.Error as ex:
        logger.error(str(ex))
        return []
    finally:
        cursor.close()
        cnx.close()
'''
