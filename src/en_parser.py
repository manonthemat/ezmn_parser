'''
en_parser.py by Matthias Sieber

As part of the EZMN Parser suite.

This program will log into your Empower Network account and get information of your leads and downline.

Don't have an account yet?
Create one here: https://www.empowernetwork.com/join.php?id=manonthemat
'''

import requests # doc: http://docs.python-requests.org/
from bs4 import BeautifulSoup # http://www.crummy.com/software/BeautifulSoup/
import emails_to_file

from configio import getlogin

def EN_get_emails(etype="basics_paid"):
    '''
    returns a list of Emails
    
    valid values for etype:
    "basics_paid"
    "basics_unpaid"
    '''
    payload = {'login': getlogin('EN', 'en_username'), 'pass': getlogin('EN', 'en_password')}
    
    session = requests.session()
    r = session.post(getlogin('EN', 'en_site'), data=payload)
    
    if r.url != 'https://www.empowernetwork.com/login.php': # login successful
        if etype == 'basics_paid':
            r = session.post('https://www.empowernetwork.com/Members/view-team.php')
        elif etype == 'basics_unpaid':
            r = session.post('https://www.empowernetwork.com/Members/view-team.php?program=U-1&submit=View+Program')
        
        emails = set()
        
        #for unpaid members (using Beautiful Soup 4)
        if 'unpaid' in etype:
            soup = BeautifulSoup(r.text).find_all('td', colspan='2')
            for email in soup:
                emails.add(email.string.strip())
                    
        #for paid members
        else:
            for x in r.text.split('<td colspan="2">'):
                s = -1 # used to find the first valid character for the Email address
                if '@' in x:
                    for i, e in enumerate(x): # getting the Email address out of the string
                        if e.isalnum() == False and e not in '<@.-_':
                            s=i
                        if e == '<': break;
                    if x[s+1:i] != '':
                        emails.add(x[s+1:i])
        
        return emails    
    
    else:
        print(r.url)
        print('Login not successful... Please check your settings in the file login_info.ini')
        return 'FAIL'
    
    
    
if __name__ == "__main__":
    print(emails_to_file.store(EN_get_emails(etype='basics_paid'), 'EN.txt', delimiter=','))
