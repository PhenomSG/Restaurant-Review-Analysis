import mysql.connector
from authentication import get_mysql_config

def get_database_connection():
    host, username, password = get_mysql_config()
    
    return mysql.connector.connect(
        host=host,
        user=username,
        password=password,
    )

connection = get_database_connection()
def is_connected():
    return connection.is_connected()

'''if connection.is_connected():
    print("Connection established to MySQL")
    print("Host:", connection.server_host)
    print("Username:", connection.user)
    print("Password:", connection._password)
else:
    print("Failed to connect to MySQL")'''
