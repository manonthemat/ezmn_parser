'''
ezmn_parser.py by Matthias Sieber

This program will log into your EZ Money Network account and get the stored
lead and membership information.

Found Email Addresses will be then stored in a text file if run by itself.
The first lines of code were written in this module.
Now it's main purpose is to provide the get_emails() function for the gui,
so users can get the emails of their leads and members within the EZ Money Network (incl. EZMF).

The EZ Money Network is a free system for GVO, PureLeverage and Empower Network affiliates.
You don't have an account yet? Sign up here: http://ezmoneynetwork.com/signup.php?user=manonthemat
'''

import requests # doc: http://docs.python-requests.org/
from configio import getlogin
import emails_to_file
from sys import argv

# funnel_ids
EZMF = 1
EZMN = 5

# lead_types
LEADS = 1
MEMBERS = 2

def get_emails(funnel=EZMF, lead_type=LEADS):
    payload = {'username': getlogin('EZMN', 'ezmn_username'), 'password': getlogin('EZMN', 'ezmn_password')}
    p2 = {'funnel_id': funnel, 'lead_type': lead_type}
        
    session = requests.session()
    r = session.post(getlogin('EZMN', 'ezmn_site'), data=payload)
    if r.url == "http://ezmoneynetwork.com/members/dashboard.php": # login successful
        # go to Lead & Member manager in business center
        r = session.post('http://ezmoneynetwork.com/members/ajax/lead_member.php', data=p2)
        data = r.text
        if '@' in data:
            ascii_only = ''
            for char in data:
                if ord(char) < 128:
                    ascii_only += char
            
            emails = set() # using a set in order to get rid of duplicate email addresses
            
            if lead_type == LEADS:
                ascii_only = ascii_only.split('<td>')
                for x in ascii_only:
                    if '@' in x:
                        if not x.startswith('<'):
                            emails.add(x[:-7]) # we don't want the '</td>' stored
                            
            else:
                ascii_only = ascii_only.split("display_info('")
                for x in ascii_only:
                    if '@' in x:
                        for i, s in enumerate(x): # searching for the first '
                            if s == "'": break;
                        emails.add(x[:i])
                
            return emails
    else:
        print('Login not successful... Please check your settings in the file login_info.py')
        return('FAIL')

def get_all():
    '''
    Getting all e-mail addresses and save them in a single file <email.txt>
    '''
    emails = set()
    for email in get_emails(funnel=EZMF, lead_type=LEADS): emails.add(email);
    for email in get_emails(funnel=EZMF, lead_type=MEMBERS): emails.add(email);
    for email in get_emails(funnel=EZMN, lead_type=LEADS): emails.add(email);
    #for email in get_emails(funnel=EZMN, lead_type=MEMBERS): emails.add(email);
    
    return emails
    
        
if __name__ == "__main__":
    if len(argv) < 3:
        if len(argv) > 1:
            if argv[1].upper() == 'ALL':
                print(emails_to_file.store(get_all(), 'emails.txt'))
                exit(0)
        print("""Usage: python3 ezmn_parser.py (FUNNEL) (LEADTYPE)
        
        FUNNEL:
            ezmn    - for EZ Money Network Leads
            ezmf    - for EZ Money Formula Leads
            ALL     - both funnels w/ leads and member emails
            
        LEADTYPE:
            leads   - for leads
            members - for members
            
        ------
        Examples:
            python3 ezmn_parser.py ezmn leads -- Gets the Email addresses of your EZMN leads
            python3 ezmn_parser.py ezmf members   -- Gets the Email addresses of your EZMF members
            python3 ezmn_parser.py all     -- Scraping and saving all unique Emails in emails.txt
        """)
        exit(0)
    if argv[1].upper() == 'EZMF':
        if argv[2].upper() == 'LEADS':
            print(emails_to_file.store(get_emails(funnel=EZMF, lead_type=LEADS), 'EZMF_leads.txt'))
        else:
            print(emails_to_file.store(get_emails(funnel=EZMF, lead_type=MEMBERS), 'EZMF_members.txt'))
    elif argv[1].upper() == 'EZMN':
        if argv[2].upper() == 'LEADS':
            print(emails_to_file.store(get_emails(funnel=EZMN, lead_type=LEADS), 'EZMN_leads.txt'))
        #else:
        #    print(emails_to_file.store(get_emails(funnel=EZMN, lead_type=MEMBERS), 'EZMN_members.txt'))
    else:
        print(emails_to_file.store(get_all(), 'emails.txt'))
