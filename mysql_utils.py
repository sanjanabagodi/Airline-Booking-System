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
    


