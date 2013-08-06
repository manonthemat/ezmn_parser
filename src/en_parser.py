'''
en_parser by Matthias Sieber

As part of the EZMN Parser suite.

This program will log into your Empower Network account and get information of your leads and downline.

Don't have an account yet?
Create one here: https://www.empowernetwork.com/join.php?id=manonthemat
'''

import requests # doc: http://docs.python-requests.orfg/
from login_info import EN_login_info

def EN_get_emails(type="basics_paid"):
    payload = {'login': EN_login_info['user'], 'pass': EN_login_info['password']}
    p2 = {} #
    
    session = requests.session()
    r = session.post(EN_login_info['site'], data=payload)
    
    if r.url == 'https://www.empowernetwork.com/Members/index.php': # login successful
        r = session.post('https://www.empowernetwork.com/Members/view-team.php', data=p2)
    
    else:
        print(r.url)
        print('Login not successful... Exiting')
        exit(0)
    
    ascii_only = ''; data = r.text;
    for char in data:
        if ord(char) < 128: ascii_only += char;
    
    emails = set()
    ascii_only = ascii_only.split('<td colspan="2">')
    for x in ascii_only:
        s = -1
        if '@' in x:
            for i, e in enumerate(x):
                if e.isalnum() == False and e is not '<' and e is not '@' and e is not '.':
                    s=i
                if e == '<': break;
            if x[s+1:i] != '':
                emails.add(x[s+1:i])
    
    print(emails)
    
if __name__ == "__main__":
    EN_get_emails()