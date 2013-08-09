import requests
from bs4 import BeautifulSoup
from login_info import RIPPLN_login_info

def Ripple_get_emails(ripple=1):
    session = requests.session()
    header = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'}
    
    # first let's get the YII_CSRF_TOKEN...
    r = session.options('http://www.startmyripple.com/site/login', headers=header)
    soup = BeautifulSoup(r.text)
    token = soup.find(type="hidden")
    token = token['value']
    payload = {'LoginForm[email]': RIPPLN_login_info['user'], 'LoginForm[password]': RIPPLN_login_info['password'], 'YII_CSRF_TOKEN':token}

    r = session.post(RIPPLN_login_info['site'], headers=header, data=payload)
    #r = session.post('http://www.startmyripple.com/ripple/index', data=payload, headers=header, allow_redirects=True)
    
    
    if r.url == 'http://www.startmyripple.com/invite/index': # login successful
        print('Success')
        payload['ripple'] = ripple
        r = session.post('http://www.startmyripple.com/ripple/godeep', headers=header, data=payload)
        data = r.text
        data = data.split('"CustomerId":')
        del data[0]
        customerIDs = []
        for id in data:
            for i, char in enumerate(id):
                if char == ',':
                    customerIDs.append(id[0:i])
                    break
        print(customerIDs)
        emails = []
        for id in customerIDs:
            payload['Id'] = str(id)
            payload['level'] = str(ripple)
            payload['caller'] = 'slider'
            payload['sort_name'] = 'DownlineCount'
            payload['sort_direction'] = '1'
            payload['page'] = '1'
            r = session.post('http://www.startmyripple.com/ajax/getCustomer', headers=header, data=payload)
            data = r.text
            data = data.split('"Email":"')
            del data[0]
            for email in data:    
                for i, char in enumerate(email):
                    if char == '"':
                        emails.append(email[0:i])
                        break
        emails = set(emails)
        print(emails)
            
    else:
        print("I'm not where I'm supposed to be... FAIL!")
        print(r.url)
        print(r.status_code)
    
if __name__ == "__main__":
    Ripple_get_emails(ripple=2)