'''
en_parser by Matthias Sieber

As part of the EZMN Parser suite.

This program will log into your Empower Network account and get information of your leads and downline.

Don't have an account yet?
Create one here: https://www.empowernetwork.com/join.php?id=manonthemat
'''

import requests # doc: http://docs.python-requests.orfg/
from bs4 import BeautifulSoup # http://www.crummy.com/software/BeautifulSoup/
import emails_to_file

from login_info import EN_login_info

def EN_get_emails(etype="basics_paid"):
    '''
    returns a list of Emails
    
    valid values for etype:
    "basics_paid"
    "basics_unpaid"
    '''
    payload = {'login': EN_login_info['user'], 'pass': EN_login_info['password']}
    
    session = requests.session()
    r = session.post(EN_login_info['site'], data=payload)
    
    if r.url == 'https://www.empowernetwork.com/Members/index.php': # login successful
        if etype == 'basics_paid':
            r = session.post('https://www.empowernetwork.com/Members/view-team.php')
        elif etype == 'basics_unpaid':
            r = session.post('https://www.empowernetwork.com/Members/view-team.php?program=U-1&submit=View+Program')
    
        data = r.text;
        ascii_only = ''
        for char in data:
            if ord(char) < 128:
                ascii_only += char
        
        emails = set()
        
        #for unpaid members (using Beautiful Soup 4)
        if 'unpaid' in etype:
            soup = BeautifulSoup(ascii_only)
            soup = soup.find_all('td', colspan='2')
            for email in soup:
                emails.add(email.string.strip())
                    
        #for paid members
        else:
            ascii_only = ascii_only.split('<td colspan="2">')
            for x in ascii_only:
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
        print('Login not successful... Please check your settings in the file login_info.py')
        exit(0)
    
    
    
if __name__ == "__main__":
    print(emails_to_file.store(EN_get_emails(etype='basics_paid'), 'EN.txt'))