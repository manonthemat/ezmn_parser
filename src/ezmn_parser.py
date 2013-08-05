'''
ezmn_parser by Matthias Sieber

This program will log into your EZ Money Network account and get the stored
lead and membership information.

Found Email Addresses will be then stored in a text file.

The EZ Money Network is a free system for GVO, PureLeverage and Empower Network affiliates.
You don't have an account yet? Sign up here: http://ezmoneynetwork.com/signup.php?user=manonthemat
'''

import requests # doc: http://docs.python-requests.org/

from login_info import login_info

payload = {'username': login_info['user'], 'password': login_info['password']}
p2 = {'funnel_id': 1, 'lead_type': 1} # we don't need 'users_id'... woohoo!!!

session = requests.session()
r = session.post(login_info['site'], data=payload)
if r.url == "http://ezmoneynetwork.com/members/dashboard.php": # login successful
    # go to Lead & Member manager in business center
    r = session.post('http://ezmoneynetwork.com/members/ajax/lead_member.php', data=p2)
    data = r.text
    if '@' in data:
        ascii_only = ''
        for char in data:
            if ord(char) < 128:
                ascii_only += char
        
        ascii_only = ascii_only.split('<td>')
        emails = {}
        emails = set(emails)
        for x in ascii_only:
            if '@' in x:
                if not x.startswith('<'):
                    emails.add(x[:-7]) # we don't want the '</td>\n' stored
        print(emails)
else:
    print('Something went wrong. Login not successful!')