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
# the database has been locally created, so omitted the above code


# helper function
def _str_datetime(val):
    return val.strftime('%Y') + '/' + val.strftime('%m') + '/' + val.strftime(
        '%d') + ' ' + val.strftime('%H') + ':' + val.strftime('%M') + ':' + val.strftime('%S')


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
    

def plan_my_trip(cxn, fname, mname, lname, dob, phno, gender, passport_no, stype, ctype, location, source, dest):
    try:
        cnx = psycopg2.connect(cnx)
        cursor = cnx.cursor()

        
        # getting id of a random travel agent
        cursor.execute("select travel_id from travelling_agent")
        travel_id = cursor.fetchone()[randrange(1,10)]
        # inserting USER details
        cursor.execute("insert into usser values(%s,%s,%s,%s,%s,%s,%s)", (fname, mname, lname, dob, phno, passport_no, travel_id))

        
        # checking if there is any scheduled trip from source to dest and gettig TRIP_ID
        cursor.execute("select count(*) from flight_trip where source = %s and dest = %s", (source, dest))
        u = cursor.fetchone()[0]
        if u > 0:
            cursor.execute("select trip_id from flight_trip where source = %s and dest = %s", (source, dest))
            trip_id = cursor.fetchone()[0]
        elif u == 0:
            # generating random trip id
            trip_id = 'T'.join(random.choices(string.ascii_uppercase, k = 3))
            time = ['07:00:00', '23:15:00', '13:00:00', '10:30:00', '04:45:00']
            dept_time = random.choice(time)
            arrival_time = random.choice(time)
            # scheduling a flight trip if it's not in the table
            cursor.execute("insert into flight_trip values (%s,%s,null,%s,%s,%s,%s)", (source, dest, dept_time, arrival_time, randrange(800, 4000), trip_id))


        # generating PNR number and adding values into BOOKING table
        pnr = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
        cursor.execute("insert into booking values (%s,%s,%s)", (travel_id, trip_id, pnr))


        # checking airplanes going from source to dest
        if u > 0:   # already exits
            cursor.execute("select airplane_no from hop where dep_airport = %s and arrival_airport = %s", (source, dest))
            airplane_no = cursor.fetchone()[0]
        if u == 0:  # doesn't exist, need to add 
            cursor.execcute("select airplane_no from airplane")
            airplane_no = cursor.fetchone()[random.randrange(1,10)]
            # generating hop_id
            hop_id = ''.join(random.choice(string.ascii_uppercase))
            hop_id = hop_id.join(random.choices(string.digits, k=3))
            # inserting HOP details
            cursor.execute("insert into hop values (%s,%s,%s,%s,%s,%s,%s)", (hop_id, random.randrange(500,2000), dept_time, arrival_time, source, dest, airplane_no))
            # inserting values into HAS
            cursor.execute("insert into has values(%s,%s)", (hop_id, trip_id))

        #inserting SEAT details
        cursor.execute("insert into seat values(%s,%s,%s,%s,%s,%s)", (randrange(1,999), stype, ctype, location, airplane_no, travel_id))
        

        list = []
        cursor.execute((discount, tax, final_amt, price, fare_type, trip_id))

    except psycopg2.Error as ex:
        logger.error(str(ex))
        return False

    
   


