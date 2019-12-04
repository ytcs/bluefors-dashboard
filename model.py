import mysql.connector
import time
import os

def read_channel(chan,num_entries,timespan=None):
    db_connection = mysql.connector.Connect(user=os.environ['CDMS_DB_USER'],password=os.environ['CDMS_DB_PWD'],host=os.environ['CDMS_DB_HOST'],port=3307,database=os.environ['CDMS_DB_NAME'])
    db_cursor = db_connection.cursor(buffered=True)

    db_cursor.execute(f'''
    SELECT
    test_db.fridgeTime,test_db.lakeshore372_{chan}
    FROM test_db
    ORDER BY test_db.fridgeTime DESC''')

    if num_entries>0:
        results = db_cursor.fetchmany(num_entries)
    else:
        results = db_cursor.fetchall()
    db_cursor.close()
    db_connection.close()
    return results





