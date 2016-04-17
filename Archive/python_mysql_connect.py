# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Contains functions for inserting/querring data from MySQL database

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
    print "data: {}".format(data)
    query = ("INSERT INTO SensorData " +
                   "(SensorType, SensorNum, Reading, Date)" +
                   " VALUES(%s, %s, %s, %s)")

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.executemany(query, [data])

        conn.commit()
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()


def insert_current_pos(data):

    # Table info: SensorData(sensorType varchar(255), sensorNum int, reading int, Date DATETIME(6))

    query = ("INSERT INTO Localization"
                "(Source, X_pos, Y_pos, Theta)"
                " VALUES(%s, %s, %s, %s);")

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


def query_sensor_data(): # Returns the last set of sensor data
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SensorData WHERE (SensorType, SensorNum, Date) IN (SELECT SensorType, SensorNum, MAX(Date) FROM SensorData GROUP BY SensorType, SensorNum)")

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
        cursor.execute("SELECT X_pos, Y_pos, Theta FROM Localization WHERE Source LIKE 'corrected' LIMIT 1")

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

if __name__ == '__main__':
    main()

'''

---------- TEST DATA ---------

CREATE TABLE SensorData(SensorType varchar(255), SensorNum int, Reading int, Date DATETIME(6));
INSERT INTO SensorData(SensorType, SensorNum, Reading, Date) VALUES 
('Sonar', 1, 10, '2015-10-26 11:38:34'), ('Sonar', 2, 10, '2015-10-26 11:38:34'), ('Sonar', 3, 10, '2015-10-26 11:38:34'),
('Light', 1, 10, '2015-10-26 11:38:34'), ('Light', 2, 10, '2015-10-26 11:38:34'), ('Light', 3, 10, '2015-10-26 11:38:34'),
('Sonar', 1, 10, '2015-10-26 11:40:18'), ('Sonar', 2, 10, '2015-10-26 11:40:18'), ('Sonar', 3, 10, '2015-10-26 11:40:18'),
('Light', 1, 10, '2015-10-26 11:40:18'), ('Light', 2, 10, '2015-10-26 11:40:18'), ('Light', 3, 10, '2015-10-26 11:40:18');


SELECT * FROM SensorData
 WHERE (SensorType, SensorNum, Date) IN
 (
   SELECT SensorType, SensorNum, MAX(Date)
     FROM SensorData
    GROUP BY SensorType, SensorNum
 )
'''
