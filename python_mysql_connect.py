from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

 
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
 
def insert_data(data):
    query = "INSERT INTO data(data_type, data_name, value, time_string, timestamp) " \
            "VALUES(%s,%s, %d, %s, %d)"
 
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

def query_commands():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM commands")
 
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

    data = [('raw', 'test_data', 1.0, '2015-09-23', 100000),
            ('raw', 'test_data', 2.0, '2015-09-23', 100000),
            ('raw', 'test_data', 3.0, '2015-09-23', 100000)]

    insert_data(data)

    query_commands()
 
if __name__ == '__main__':
    main()