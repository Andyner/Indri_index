import MySQLdb

def connect(dbname):
    conn = MySQLdb.connect(user='oopin',passwd='OOpin2007Group',db=dbname,host='192.168.241.29');
    return conn

def close(conn):
    conn.cursor().close()
    conn.close()
    
def query_many(conn,sql):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except:
        raise Exception('sql error') 

    

    
