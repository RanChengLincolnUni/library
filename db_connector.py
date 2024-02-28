from MySQLdb import MySQLError
import mysql.connector

db_congfig = dict(
    user="root",
    password="Woshizhongguoren",
    host="localhost",
    port="3306",
    database="library",
)


def connection():
    try:
        connection = mysql.connector.connect(
            **db_congfig,
            autocommit=True,
        )
        return connection
    except MySQLError:
        # print(error)
        return None


def close():
    """global _connection, _cursor
    if _cursor is not None:
        _cursor.close()
    if _connection is not None:
        _connection.close()"""
    pass
