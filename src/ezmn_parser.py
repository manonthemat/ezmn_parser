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
from sys import argv

# funnel_ids
EZMF = 1
EZMN = 5

# lead_types
# TODO: The HTML document for members is formatted differently. Parsing for email-addresses there does not work yet
LEADS = 1
MEMBERS = 2

def get_emails(funnel=EZMN, lead_type=LEADS):
    payload = {'username': login_info['user'], 'password': login_info['password']}
    p2 = {'funnel_id': funnel, 'lead_type': lead_type}
    
    if funnel == EZMN or funnel == 'EZMN':
        funnelname = 'EZMN'
    elif funnel == EZMF or funnel == 'EZMF':
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
            return funnelname+'.txt'
            
    else:
        print('Something went wrong. Login not successful!')

def get_all():
    '''
    Getting all e-mail addresses and save them in a single file <email.txt>
    '''
    ezmn_file = open(get_emails(funnel=EZMN), 'r')
    ezmf_file = open(get_emails(funnel=EZMF), 'r')
    emails = set()
    for email in ezmn_file.readlines():
        emails.add(email)
    ezmn_file.close()
    for email in ezmf_file.readlines():
        emails.add(email)
    ezmf_file.close()
    email_file = open('emails.txt','w')
    for i, email in enumerate(emails):
        email_file.write(email)
    email_file.close()
    print(i+1, "unique email addresses stores in 'emails.txt'")
    
        
if __name__ == "__main__":
    if len(argv) < 2:
        print("""Usage: python3 ezmn_parser.py (FUNNEL)
        
        FUNNEL:
            ezmn - for EZ Money Network Leads
            ezmf - for EZ Money Formula Leads
            ALL
            
        ------
        Examples:
            python3 ezmn_parser.py ezmn    -- Gets the Email addresses of your EZMN leads
            python3 ezmn_parser.py ezmf    -- Gets the Email addresses of your EZMF leads
            python3 ezmn_parser.py all     -- Getting leads from both funnels and store unique Emails in emails.txt
        """)
        exit(0)
    if argv[1].upper() == 'EZMF': get_emails(funnel=EZMF);
    elif argv[1].upper() == 'EZMN': get_emails(funnel=EZMN);
    else: get_all()