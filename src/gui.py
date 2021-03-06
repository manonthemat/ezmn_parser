'''
gui.py by Matthias Sieber

Graphical User Interface for the different parser modules
and the starting point for the average user.

TODO: Make it pretty.
'''

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showwarning, showerror

import webbrowser

import ezmn_parser
import en_parser
import emails_to_file
import ripple_parser
from configio import getlogin, setlogin, getdelimiter, setdelimiter

class Application(Frame):
    delimiter = getdelimiter()
            
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
            
    def createWidgets(self):
        mainframe = Frame(self)
        mainframe.grid(column=0, row=0, sticky=N+S+W+E, padx=10, pady=10)
        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)
        
        ttk.Label(mainframe, text='Get Email addresses from...').grid(column=0, row=0, sticky=W)
        
        self.ezmf_leads = StringVar()
        self.ezmf_members = StringVar()
        self.ezmn_leads = StringVar()
        self.en_basics_paid = StringVar()
        self.en_basics_unpaid = StringVar()
        self.rippln_leads = StringVar()
        ttk.Checkbutton(mainframe, text='EZ Money Formula Leads', variable=self.ezmf_leads).grid(column=0, row=1, sticky=W)
        ttk.Checkbutton(mainframe, text='EZ Money Formula Members', variable=self.ezmf_members).grid(column=0, row=2, sticky=W)
        ttk.Checkbutton(mainframe, text='EZ Money Network Leads', variable=self.ezmn_leads).grid(column=0, row=3, sticky=W)
        ttk.Checkbutton(mainframe, text='Empower Network Basic Members (paid)', variable=self.en_basics_paid).grid(column=0, row=4, sticky=W)
        ttk.Checkbutton(mainframe, text='Empower Network Members (unpaid)', variable=self.en_basics_unpaid).grid(column=0, row=5, sticky=W)
        ttk.Checkbutton(mainframe, text='Rippln (this may take a few minutes)', variable=self.rippln_leads).grid(column=0, row=6, sticky=W)
        ttk.Button(mainframe, text='Collect Emails', command=self.collect).grid(column=0, row=7, columnspan=2, pady=10)
        
        ttk.Label(mainframe, text='Collected Email addresses below...', padding='0 20 0 0').grid(column=0, row=8, columnspan=2)
        
        self.emailbox = Text(mainframe)
        self.emailbox.grid(column=0, row=9, columnspan=2)
        
        self.amount_emails = IntVar()
        ttk.Label(mainframe, textvariable=self.amount_emails).grid(column=0, row=10, sticky=E)
        ttk.Label(mainframe, text='unique Emails collected').grid(column=1, row=10)
        
        ### Menu
        root.option_add('*tearOff', FALSE)
        
        menubar = Menu(root)
        root.config(menu=menubar)
        
        menu_file = Menu(menubar)
        menu_file.add_command(label='Save as...', command=self.saveToFile)
        menu_file.add_command(label='Settings', command=self.openSettings)
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=exit)
        menubar.add_cascade(menu=menu_file, label='File')

        
    def collect(self):
        emails = set()
        ezmf_leads = self.ezmf_leads.get()
        ezmf_members = self.ezmf_members.get()
        ezmn_leads = self.ezmn_leads.get()
        en_basics_paid = self.en_basics_paid.get()
        en_basics_unpaid = self.en_basics_unpaid.get()
        rippln_leads = self.rippln_leads.get()
        
        login_error = set()
        
        if ezmf_leads == '1':
            mails = ezmn_parser.get_emails()
            if mails != 'FAIL':
                emails.update(mails)
            else:
                login_error.add('EZ Money Network')
        if ezmf_members == '1':
            mails = ezmn_parser.get_emails(funnel=1, lead_type=2)
            if mails != 'FAIL':
                emails.update(mails)
            else:
                login_error.add('EZ Money Network')
        if ezmn_leads == '1':
            mails = ezmn_parser.get_emails(funnel=5, lead_type=1)
            if mails != 'FAIL':
                emails.update(mails)
            else:
                login_error.add('EZ Money Network')
        if en_basics_paid == '1':
            mails = en_parser.EN_get_emails(etype="basics_paid")
            if mails != 'FAIL':
                emails.update(mails)
            else:
                login_error.add('Empower Network')
        if en_basics_unpaid == '1':
            mails = en_parser.EN_get_emails(etype="basics_unpaid")
            if mails != 'FAIL':
                emails.update(mails)
            else:
                login_error.add('Empower Network')
        if rippln_leads == '1':
            for i in range(1, 13):
                mails = ripple_parser.Ripple_get_emails(ripple=i)
                if mails != 'FAIL':
                    emails.update(mails)
                else:
                    login_error.add('Rippln')
                    break
        
        try:
            if len(login_error) > 0:
                error_title = 'Login not successful'
                error_message = 'Please check your '+', '.join(login_error)+' settings'
                showerror(error_title, error_message)
        except:
            pass
        
        self.emailbox.delete(1.0, END)
        for i, email in enumerate(emails):
            self.emailbox.insert(END, email+'\n')
        self.amount_emails.set(i+1)
        
        

    def saveToFile(self):
        # check if Emails are collected
        if len(self.emailbox.get(1.0, END)) > 1:
            # open File Dialog
            filename = filedialog.asksaveasfile()
            # call emails_to_file.store
            emails_to_file.store_from_gui(self.emailbox.get(1.0, END), filename.name, delimiter=self.delimiter)
        else:
            # Show warning when 'save as...' is selected prior of collecting emails
            showwarning('User advice', 'Collect Emails first, before you save them.')
    
    def openSettings(self):
        self.settingswindow = Toplevel(self)
        self.settingswindow.title('Settings')
        delimiterframe = ttk.Labelframe(self.settingswindow, text='Delimiter', padding='30 10 10 10')
        delimiterframe.grid(column=0, row=0, pady=10)
        self.rDelimiter = StringVar()
        self.rDelimiter.set(self.delimiter)
        ttk.Radiobutton(delimiterframe, text='new line', variable=self.rDelimiter, value='\n').grid(column=0, row=0, sticky=W)
        ttk.Radiobutton(delimiterframe, text='comma', variable=self.rDelimiter, value=',').grid(column=0, row=1, sticky=W)
        ttk.Radiobutton(delimiterframe, text='whitespace', variable=self.rDelimiter, value=' ').grid(column=0, row=2, sticky=W)
        
        ezmnframe = ttk.Labelframe(self.settingswindow, text='EZ Money Network', padding='30 10 10 10')
        ezmnframe.grid(column=0, row=1, pady=10, padx=5)
        ttk.Label(ezmnframe, text='Username:').grid(column=0, row=0, sticky=W)
        ttk.Label(ezmnframe, text='Password:').grid(column=0, row=1, sticky=W)
        ttk.Label(ezmnframe, text="No account?").grid(column=0, row=2, sticky=W)
        self.ezmn_user = StringVar()
        self.ezmn_user.set(getlogin('EZMN', 'ezmn_username'))
        self.ezmn_pw = StringVar()
        self.ezmn_pw.set(getlogin('EZMN', 'ezmn_password'))
        ttk.Entry(ezmnframe, textvariable=self.ezmn_user, width=26).grid(column=1, row=0, sticky=W)
        ttk.Entry(ezmnframe, textvariable=self.ezmn_pw, width=26, show='*').grid(column=1, row=1, sticky=W)
        ttk.Button(ezmnframe, text="Sign up (FREE)!", command=self.join_ezmf).grid(column=1, row=2, sticky=W)
        
        enframe = ttk.Labelframe(self.settingswindow, text='Empower Network', padding='30 10 10 10')
        enframe.grid(column=0, row=2, pady=10, padx=5)
        ttk.Label(enframe, text='Username:').grid(column=0, row=0, sticky=W)
        ttk.Label(enframe, text='Password:').grid(column=0, row=1, sticky=W)
        ttk.Label(enframe, text="No account?").grid(column=0, row=2, sticky=W)
        self.en_user = StringVar()
        self.en_user.set(getlogin('EN', 'en_username'))
        self.en_pw = StringVar()
        self.en_pw.set(getlogin('EN', 'en_password'))
        ttk.Entry(enframe, textvariable=self.en_user, width=26).grid(column=1, row=0, sticky=W)
        ttk.Entry(enframe, textvariable=self.en_pw, width=26, show='*').grid(column=1, row=1, sticky=W)
        ttk.Button(enframe, text="Sign up here!", command=self.join_en).grid(column=1, row=2, sticky=W)        
        
        ripplnframe = ttk.Labelframe(self.settingswindow, text='Rippln', padding='30 10 10 10')
        ripplnframe.grid(column=0, row=3, pady=10, padx=5)
        ttk.Label(ripplnframe, text='Email:').grid(column=0, row=0, sticky=W)
        ttk.Label(ripplnframe, text='Password:').grid(column=0, row=1, sticky=W)
        ttk.Label(ripplnframe, text="No account?").grid(column=0, row=2, sticky=W)
        self.rippln_user = StringVar()
        self.rippln_user.set(getlogin('RIPPLN', 'rippln_username'))
        self.rippln_pw = StringVar()
        self.rippln_pw.set(getlogin('RIPPLN', 'rippln_password'))
        ttk.Entry(ripplnframe, textvariable=self.rippln_user, width=26).grid(column=1, row=0, sticky=W)
        ttk.Entry(ripplnframe, textvariable=self.rippln_pw, width=26, show='*').grid(column=1, row=1, sticky=W)
        ttk.Button(ripplnframe, text="Sign up here!", command=self.join_rippln).grid(column=1, row=2, sticky=W)
        
        ttk.Button(self.settingswindow, text='Save settings', command=self.saveSettings).grid(column=0, row=100, pady=10)
        
        self.settingswindow.focus()
        
    def saveSettings(self):
        self.delimiter = self.rDelimiter.get()
        setlogin('EZMN','ezmn_username', self.ezmn_user.get())
        setlogin('EZMN','ezmn_password', self.ezmn_pw.get())
        setlogin('EN','en_username', self.en_user.get())
        setlogin('EN','en_password', self.en_pw.get())
        setlogin('RIPPLN','rippln_username', self.rippln_user.get())
        setlogin('RIPPLN','rippln_password', self.rippln_pw.get())
        setdelimiter(self.delimiter)
        self.settingswindow.destroy()
        
    def join_en(self):
        webbrowser.open('https://www.empowernetwork.com/join.php?id=manonthemat', autoraise=True)
        
    def join_ezmf(self):
        webbrowser.open('http://ezmoneynetwork.com/signup.php?user=manonthemat', autoraise=True)
        
    def join_rippln(self):
        webbrowser.open('http://www.startmyripple.com/blitzlink/792e3c8bc5586a588a0fca7e3f17f4be', autoraise=True)

if __name__ == "__main__":
    root = Tk()
    root.title('EZ Email Parser')
    app = Application(master=root)
    app.mainloop(0)
