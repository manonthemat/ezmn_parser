import configparser

def getlogin(funnel, data):
    """returns the value of data in section funnel of the 'login_info.ini'"""
    config = configparser.ConfigParser()
    config.read('login_info.ini')
    return config[funnel][data]

if __name__ == "__main__":
    print(getlogin('EN', 'EN_USERNAME'))