import mysql.connector
import time
import os
import itertools
import datetime

def get_channels():
    db_connection = mysql.connector.Connect(
        user=os.environ['CDMS_DB_USER'], password=os.environ['CDMS_DB_PWD'], host=os.environ['CDMS_DB_HOST'], port=3306, database=os.environ['CDMS_DB_NAME'])
    db_cursor = db_connection.cursor(buffered=True)

    db_cursor.execute('''
    SELECT DISTINCT channel
    FROM bluefors''')

    results = db_cursor.fetchall()
    db_cursor.close()
    db_connection.close()
    return list(itertools.chain(*results))


def read_channel(chan, num_entries, timespan=None):
    db_connection = mysql.connector.Connect(
        user=os.environ['CDMS_DB_USER'], password=os.environ['CDMS_DB_PWD'], host=os.environ['CDMS_DB_HOST'], port=3306, database=os.environ['CDMS_DB_NAME'])
    db_cursor = db_connection.cursor(buffered=True)

    db_cursor.execute(f'''
    SELECT
    fridgeTime,reading
    FROM bluefors
    WHERE fridgeTime >= NOW() - INTERVAL 1 DAY
    AND channel = "{chan}"
    ORDER BY fridgeTime DESC''')

    if num_entries > 0:
        results = db_cursor.fetchmany(num_entries)
    else:
        results = db_cursor.fetchall()
    db_cursor.close()
    db_connection.close()
    results= list(zip(*results))
    #convert timezone from UTC to PST
    return [dt+datetime.timedelta(hours=-8) for dt in results[0]],list(results[1])
