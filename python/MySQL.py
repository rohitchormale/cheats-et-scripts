'''
1. import MySQLdb

2. Create connection object with provding (serveraddrs,loginname,passw,dbname)
    db = MySQLdb.connect(host,user,pass,database)

    important methods:
    db.commit()
    db.rollback()
    db.cursor()
    db.close()
    
3. Create cursor object
    fire = db.cursor()

4. Write Query (optional)
    one can provide query directly along with execute method of cursor object.
    for longer queries, better create query separately
    ex. query = """ creat table hello(
                    ...
                    )
                    """
    Also with this approach we can provide dynamic data to query
    ex. query = """create table %s(
                    ...
                    )
                    """ % (hello)
    
5. Excecute query using cursor object's execute method
    ex. fire.execute('select * from student')
        fire.execute(query)
        db.commit
        db.rollback
        
6. Fetch data if required
    fetchone(),fetchall(),rowcount()
    First access each row like sequence and then to access column, provide index
    ex. for row in fire.fetchall():
            sno = row[0]
            sname = row[1]
            
7. Close connection
    db.close()
'''

#1 import MySQLdb
import MySQLdb
#2 create connection
db = MySQLdb.connect("<host addr>","<username>","<password>","<dbname>")
#3 create cursor object
fire = db.cursor()
#4 create query
query = '''insert into <tablename>(
            %s datatype options
            %s datatype options
            %s datatype options
            ...
            PRIMARY KEY(col1...)
            )
            ''' % (col1,col2,col3)

#5 execute query
try:
    fire.execute(query)
    db.commit()
except:
    db.rollback()
    
#6 fetch data
    fire.execute('select * from <tablename>')
try:
    data = fire.fetchall
    for row in data:
        a = row[0]
        b = row[1]
        c = row[2]
        print fno,fname,fadd
except:
    print 'Error: unable to fetch data'

#7 close connection
db.close()
