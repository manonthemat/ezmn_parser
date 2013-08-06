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

# funnel_ids
EZMF = 1
EZMN = 5

# lead_types
# TODO: The HTML document for members is formatted differently. Parsing for email-addresses does not work yet
LEADS = 1
MEMBERS = 2

def get_emails(funnel=EZMN, lead_type=LEADS):
    payload = {'username': login_info['user'], 'password': login_info['password']}
    p2 = {'funnel_id': funnel, 'lead_type': lead_type}
    
    if funnel == EZMN:
        funnelname = 'EZMN'
    elif funnel == EZMF:
        funnelname = 'EZMF'
    else:
        funnelname = 'emails'
    
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
            emails = set() # using a set first in order to get rid of duplicate emails
            email_file = open(funnelname+'.txt','w')
            for x in ascii_only:
                if '@' in x:
                    if not x.startswith('<'):
                        emails.add(x[:-7]) # we don't want the '</td>' stored
            for i, email in enumerate(emails):
                email_file.write(email+'\n')
            print(i+1, "Emails saved in '"+funnelname+".txt'")
            email_file.close()
            
    else:
        print('Something went wrong. Login not successful!')
        
if __name__ == "__main__":
    get_emails(funnel=5)