import configparser

def get_mysql_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    host = config['mysql']['host']
    username = config['mysql']['username']
    password = config['mysql']['password']
    
    return host, username, password

'''connection = get_mysql_config()
print(connection)
print("Host:", connection[0])
print("Username:", connection[1])
print("Password:", connection[2])'''
