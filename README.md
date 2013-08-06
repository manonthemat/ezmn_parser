ezmn_parser by Matthias Sieber
Started on August 5th of 2013. First working version on the same day (of course).

This program will log into your EZ Money Network account and get the stored
lead and membership information.

Found Email Addresses are stored in a text file.

The EZ Money Network is a free system for GVO, PureLeverage and Empower Network affiliates.
You don't have an account yet? Sign up here: http://ezmoneynetwork.com/signup.php?user=manonthemat

Set your USERNAME and PASSWORD in src/login_info.py


REQUIREMENTS
=============================
- Python 3.3.2 or newer
- Requests (tested with v.1.2.3) http://docs.python-requests.org/
- Beautiful Soup 4.2.0 (for en_parser.py) http://www.crummy.com/software/BeautifulSoup/

TODO
=============================
- Improving usability
- Build a GUI
- Refactor code
- Support different formats for scraped email addresses
