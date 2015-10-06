from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import datetime


def connect():
    """ Connect to MySQL database """

    db_config = read_db_config()

    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')

    except Error as error:
        print(error)

    finally:
        conn.close()
        print('Connection closed.')


def insert_sensor_data(data):

    # Table info: SensorData(sensorType varchar(255), sensorNum int, reading int, Date DATETIME(6))

    query = "INSERT INTO SensorData(sensorType, sensorNum, reading, date) " \
            "VALUES(%s, %d, %d, %s)"

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.executemany(query, data)

        conn.commit()
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()

def insert_current_pos():

    # Table info: SensorData(sensorType varchar(255), sensorNum int, reading int, Date DATETIME(6))

    query = "INSERT INTO Localization(type, x_pos, y_pos, theta) VALUES(%s, %d, %d, %d)"

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.executemany(query, data)

        conn.commit()
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()

def query_map():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT x_pos, y_pos FROM Map") # TODO: Make consistent with database

        row = cursor.fetchall()

        while row is not None:
            print(row)
            row = cursor.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return row


def query_current_pos():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT x_pos, y_pos, theta FROM Localization WHERE type = robotpose") # TODO: Make consistent with database

        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return row


def main():

    connect()

    data = [('test', 1, 10.0, datetime.datetime.now()),
            ('test', 1, 10.0, datetime.datetime.now()),
            ('test', 1, 10.0, datetime.datetime.now())]

    insert_sensor_data(data)

    query_commands()

if __name__ == '__main__':
    main()
