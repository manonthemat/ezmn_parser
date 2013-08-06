'''
emails_to_file.py by Matthias Sieber
'''

def store(email_list, filename):
    '''takes a list of strings and stores them in a file'''
    f = open(filename, 'w')
    for i, email in enumerate(email_list):
        f.write(email+'\n')
    f.close()
    return str(i+1)+' Emails stored in '+filename