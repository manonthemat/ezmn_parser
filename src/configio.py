'''
configio.py by Matthias Sieber

configio has two functions which use python's built-in module configparser
to read and write values for pre-set attributes in the file login_info.ini,
where login information is stored for several affiliate programs.

The getlogin function is used in every parser-file within ezmn_parser,
to gain access to the websites in order to be able to collect the information
from those sites.

The setlogin function is used in the settings-menu of the gui.
Please be aware that calling setlogin() removes all the comments in the login_info.ini
and attributes (keys) will be lowercase.

TODO: Read/Write the delimiter into the config file, too.
'''

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
    print('Your EN Username:', getlogin('EN', 'en_username'))
    uin = input('Set your EZMN Username: ')
    setlogin('EZMN', 'ezmn_username', uin)