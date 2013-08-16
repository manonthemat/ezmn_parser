import configparser

def getlogin(funnel, data):
    """returns the value of data in section funnel of file 'login_info.ini'"""
    config = configparser.ConfigParser()
    config.read('login_info.ini')
    return config[funnel][data]

def setlogin(funnel, data, value):
    """sets value for data in section funnel of file 'login_info.ini'"""
    config = configparser.ConfigParser()
    config.read('login_info.ini')
    config[funnel][data] = value
    with open('login_info.ini', 'w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    print('Your EN Username:', getlogin('EN', 'EN_USERNAME'))
    uin = input('Set your EZMN Username: ')
    setlogin('EZMN', 'EZMN_USERNAME', uin)