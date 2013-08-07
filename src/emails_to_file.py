'''
emails_to_file.py by Matthias Sieber
'''

def store(email_list, filename, delimiter='\n'):
    '''takes a list of strings and stores them in a file'''
    f = open(filename, 'w')
    for i, email in enumerate(email_list):
        f.write(email+delimiter)
    f.close()
    return str(i+1)+' Emails stored in '+filename

def store_from_gui(emails, filename, delimiter='\n'):
    '''emails - a string (usually from gui's emailbox of class Application)'''
    if delimiter != '\n':
        f = open(filename, 'w')
        f.write(emails)
        f.close()
    else:
        email_list = emails.split()
        store(email_list, filename, delimiter=delimiter)
