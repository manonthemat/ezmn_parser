'''
ripple_parser.py by Matthias Sieber

This program will log into your Rippln account and get email addresses of your 'ripple'.

As of right now this is the slowest parser within the ezmn_parser suite (which really should be renamed)
due to the many requests that are being sent.

It's also noteworthy that the startmyripple.com website has a csrf protection which was new to me.
'''

import requests
from bs4 import BeautifulSoup
from configio import getlogin
import emails_to_file

def Ripple_get_emails(ripple=1):
    session = requests.session()
    header = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'}
    
    # first let's get the YII_CSRF_TOKEN...
    r = session.options('http://www.startmyripple.com/site/login', headers=header)
    soup = BeautifulSoup(r.text)
    token = soup.find(type="hidden")
    token = token['value']
    payload = {'LoginForm[email]': getlogin('RIPPLN', 'rippln_username'),
               'LoginForm[password]': getlogin('RIPPLN', 'rippln_password'),
               'YII_CSRF_TOKEN':token}

    r = session.post(getlogin('RIPPLN', 'rippln_site'), headers=header, data=payload)
    
    
    if r.url == 'http://www.startmyripple.com/invite/index': # login successful
        print('Success')
        customerIDs = []
        payload['ripple'] = ripple
        for page in range(1,20): # TODO: adjust range, so that all customerIDs are captured without running the loop too often
            payload['page'] = page
            r = session.post('http://www.startmyripple.com/ripple/godeep', headers=header, data=payload)
            data = r.text.split('"CustomerId":')
            del data[0]
            
            for r_id in data:
                for i, char in enumerate(r_id):
                    if char == ',':
                        customerIDs.append(r_id[0:i])
                        break
        emails = []
        for r_id in customerIDs:
            payload['Id'] = str(r_id)
            payload['level'] = str(ripple)
            r = session.post('http://www.startmyripple.com/ajax/getCustomer', headers=header, data=payload)
            data = r.text.split('"Email":"')
            
            for i, char in enumerate(data[1]):
                if char == '"':
                    emails.append(data[1][0:i])
                    break
        emails = set(emails)
        return emails
            
    else:
        print('Login not successful... Please check your settings in the file login_info.ini')
        return 'FAIL'
    
if __name__ == "__main__":
    result = set()
    for x in range(1, 13):
        result.update(Ripple_get_emails(ripple=x))
    print(emails_to_file.store(result, 'rippln.txt'))
        