'''
Graphical User Interface for the parser
'''

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showwarning

import ezmn_parser
import en_parser
import emails_to_file

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
            
    def createWidgets(self):
        mainframe = Frame(self)
        mainframe.grid(column=0, row=0, sticky=N+S+W+E)
        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)
        
        ttk.Label(mainframe, text='Get Email addresses from...').grid(column=0, row=0, sticky=W)
        
        self.ezmf_leads = StringVar()
        self.ezmf_members = StringVar()
        self.ezmn_leads = StringVar()
        self.en_basics_paid = StringVar()
        self.en_basics_unpaid = StringVar()
        ttk.Checkbutton(mainframe, text='EZ Money Formula Leads', variable=self.ezmf_leads).grid(column=0, row=1, sticky=W)
        ttk.Checkbutton(mainframe, text='EZ Money Formula Members', variable=self.ezmf_members).grid(column=0, row=2, sticky=W)
        ttk.Checkbutton(mainframe, text='EZ Money Network Leads', variable=self.ezmn_leads).grid(column=0, row=3, sticky=W)
        ttk.Checkbutton(mainframe, text='Empower Network Basic Members (paid)', variable=self.en_basics_paid).grid(column=0, row=4, sticky=W)
        ttk.Checkbutton(mainframe, text='Empower Network Members (unpaid)', variable=self.en_basics_unpaid).grid(column=0, row=5, sticky=W)
        
        ttk.Button(mainframe, text='Collect Emails', command=self.collect).grid(column=0, row=6, columnspan=2)
        
        ttk.Label(mainframe, text='Collected Email addresses below...', padding='0 20 0 0').grid(column=0, row=7, columnspan=2)
        
        self.emailbox = Text(mainframe)
        self.emailbox.grid(column=0, row=8, columnspan=2)
        
        self.amount_emails = IntVar()
        ttk.Label(mainframe, textvariable=self.amount_emails).grid(column=0, row=9, sticky=E)
        ttk.Label(mainframe, text='unique Emails collected').grid(column=1, row=9)
        
        ### Menu
        root.option_add('*tearOff', FALSE)
        
        menubar = Menu(root)
        root.config(menu=menubar)
        
        menu_file = Menu(menubar)
        menu_file.add_command(label='Save as...', command=self.saveToFile)
        #menu_file.add_command(label='Settings', command=self.openSettings)
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=exit)
        menubar.add_cascade(menu=menu_file, label='File')
        self.pack()
        
    def collect(self):
        emails = set()
        ezmf_leads = self.ezmf_leads.get()
        ezmf_members = self.ezmf_members.get()
        ezmn_leads = self.ezmn_leads.get()
        en_basics_paid = self.en_basics_paid.get()
        en_basics_unpaid = self.en_basics_unpaid.get()
        
        if ezmf_leads == '1':
            emails.update(ezmn_parser.get_emails())
        if ezmf_members == '1':
            emails.update(ezmn_parser.get_emails(funnel=1, lead_type=2))
        if ezmn_leads == '1':
            emails.update(ezmn_parser.get_emails(funnel=5, lead_type=1))
        if en_basics_paid == '1':
            emails.update(en_parser.EN_get_emails(etype="basics_paid"))
        if en_basics_unpaid == '1':
            emails.update(en_parser.EN_get_emails(etype="basics_unpaid"))
        
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
            emails_to_file.store_from_gui(self.emailbox.get(1.0, END), filename.name)
        else:
            # Show warning when 'save as...' is selected prior of collecting emails
            showwarning('User advice', 'Collect Emails first, before you save them.')
    def openSettings(self):
        pass

root = Tk()
root.title('EZ Email Parser')
app = Application(master=root)
app.mainloop(0)