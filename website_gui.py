import tkinter as tk
import website_copier as wc
from tkinter import messagebox as mb

#TODO: catch IOError from website connection, which is login error
#      make enter automaitcally log you in
#      default text pointer to the login box

class website_gui:

    def __init__(self, rl):
        self.window = tk.Tk()
        self.window.title("Wiki Copy Tool")
        self.row_length = rl
        self.wikis={}
        self.sa = True

    def login(self, first_time = True):
        self.window.resizable(width=False, height=False)
        self.window.geometry('{}x{}'.format(500, 500))
        self.forget()
        s = 'Please Login'
#        if not first_time:
#            s = 'Incorrect Login'
        l = tk.Label(self.window, text=s, pady = 50, padx = 40, font = "Helveltica 30")
        l.grid(row=0, column=0, columnspan=2)
        
        self.user = tk.StringVar()
        self.pswd = tk.StringVar()
        login = tk.Label(self.window, text='User:')
        password = tk.Label(self.window, text='Password:')
        login.grid(row=1, column=0, pady = 10)
        password.grid(row=2, column=0, pady = 10)
        logintxt = tk.Entry(self.window, textvariable=self.user)
        passwordtxt = tk.Entry(self.window, textvariable=self.pswd, show = '*')
        logintxt.grid(row=1, column=1, pady = 10)
        passwordtxt.grid(row=2, column=1, pady = 10)

        btn = tk.Button(self.window, text = "LOGIN", command = lambda event: self.main_window(first_time))
        self.window.bind('<Return>', lambda event: self.main_window(first_time))
        btn.grid(row=3, column=0, columnspan=2, pady = 30)
        self.window.mainloop()

    def main_window(self, first_time = True):
        self.window.resizable(width=True, height=True)
        self.window.geometry('')
        self.forget()
        l = tk.Label(self.window, text='Source Text URL: ')
        l.grid(row=0, column=0)
        self.src = tk.StringVar()
        sourcetxt = tk.Entry(self.window, textvariable=self.src, width = 150)
        sourcetxt.grid(row=0, column=1, columnspan = self.row_length - 1)
        self.selection(first_time)
        btn1 = tk.Button(self.window, text = "Copy my page", command = self.copy)
        self.window.bind('<Return>', self.copy)
        btn1.grid(row = len(self.wikis) // self.row_length + 2, column = self.row_length//2)

    def copy(self, event = None):
        try:
            self.get_wikis()
            if self.src.get() == '':
                mb.showwarning('Missing Information', 'Missing source url')
                self.main_window(False)
                return
            self.w = wc.website_copier(self.user.get(), self.pswd.get(), self.src.get(), destination_wikis=self.destination_wikis)
            self.w.copy()
        except IOError:
            mb.showerror('Error', 'Login Incorrect or No Permission')
            self.login(False)

    def get_wikis(self):
        self.destination_wikis = [self.reference_wikis[wiki] for wiki in self.wikis if self.wikis[wiki].get()]
        print(self.destination_wikis)

    def selection(self, first_time = True):
        i = 0
        self.reference_wikis = wc.get_wikis()
        for wiki in self.reference_wikis:
            if first_time:
                self.wikis[wiki] = tk.BooleanVar()
            l = tk.Checkbutton(self.window, text=wiki, variable = self.wikis[wiki], justify = 'left')
            l.grid(row = i // self.row_length + 1, column = i % self.row_length)
            i += 1
        l = tk.Checkbutton(self.window, text='select all', command=lambda: self.update_select())
        l.grid(row = i // self.row_length + 2, column = self.row_length + 1)

    def checkbox(self, wiki):
        self.wikis[wiki].set(not self.wikis[wiki])

    def all(self):
        for v in self.wikis.values():
            print(v.get())

    #clears the window
    def forget(self):
        for widget in self.window.winfo_children():
            widget.grid_forget()
    
    def update_select(self):
        for wiki in self.wikis:
            self.wikis[wiki].set(self.sa)
        self.sa = not self.sa
            
wb = website_gui(7)
wb.login()
