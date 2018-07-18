from psycopg2 import pool


class Database:

    __connection_pool = None  # not beloning to a object but beloning to a class, it is static the __ is used to make
                              # the variable private and not accesable outside of the database class

    @staticmethod # we could also use, class metod and pass in cls
    def initialise(**kwargs):
        Database.__connection_pool = pool.SimpleConnectionPool(1,  # this exsists outside of the connection from pool class
                                                             10,
                                                             **kwargs
                                                             )

    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()

    @classmethod
    def put_connection(cls, connection):
        return cls.__connection_pool.putconn(connection)

    @staticmethod
    def close_all_connections():
        Database.__connection_pool.closeall()

# is the old way of doing it, the most expensive part of the conneciton is operning or closeing, so we use the above
# def connect():
#     return psycopg2.connect(user='postgres', password='StugerPest**', database='learning', host='localhost')


class CursorFromConnectionFromPool:

    def __init__(self): # when we initilise the object this is called, and so doenot create the conneciton
        self.connection = None
        self.cursor = None

    def __enter__(self): # when we enter the with, this is called
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()

        return self.cursor

    def __exit__(self, exc_type, exception_value, exc_tb): # when we exit the with this is called
        if exception_value is not None:  # if we have any errors in the with clause, then roll back the changes.
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.put_connection(self.connection) # we use the put con method of the connection pool to retutn the connection


