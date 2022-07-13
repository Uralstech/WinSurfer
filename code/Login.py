"""
Author: Udayshankar R
GitHub: https://github.com/Uralstech

This helps WinSurfer with loggin in!

"""

from ShrtCde.InDev.UI import *
from FileAccessors.WSEFOpener import *
from Encryptor import Encryptor
from USER import USER
import re
import os

local_encryptor = Encryptor()

def Start():
    path = os.getcwd() + r"\Data\User_data.wsef"

    def Login():
        def check_user():
            for i in USER.all:
                if i.username == username.get() and i.password == local_encryptor.encrypt_string(password.get()):
                    USER.logged_user = i
                    root2.destroy()
                    return
            showerror("WinSurfer Login", "There was an error while loggin in. Please make sure your account exists and that your password is correct.")

        root.destroy()
        root2 = GetRoot("WinSurfer Login", "200x190", "black", None)
        root2.resizable(False, False)

        username = StringVar(root2)
        password = StringVar(root2)

        tfont = GetFont("Terminal", 12)
        GetLabel(root2, "Username", font=tfont, colour="White", bgcolour="Black").pack(pady=10, padx=10, anchor=W)
        GetEntry(root2, username, "DEFAULTUSER", 14, tfont, "Black", "White", 0, 1, "White")
        GetLabel(root2, "Password", font=tfont, colour="White", bgcolour="Black").pack(pady=10, padx=10, anchor=W)
        GetEntry(root2, password, "DefUsr123#", 14, tfont, "Black", "White", 0, 1, "White")['show'] = '*'
        GetButton(root2, "Log in", width=9, font=GetFont("Terminal", 20, "bold"), bgColour="Black", fgColour="White", function=check_user).pack(pady=10)

        root2.mainloop()
    def Signin():
        def check_user():
            for i in USER.all:
                if i.username == username.get():
                    showerror("WinSurfer Sign in", "There was an error while creating your account. Please make sure your username is unique.")
                    return
            
            if len(username.get()) < 4:
                showerror("WinSurfer Sign in", "There was an error while creating your account. Please make sure your username has at least four characters.")
                return
            
            if password.get() != confirmed_password.get():
                showerror("WinSurfer Sign in", "There was an error while creating your account. Please make sure that your password is the same in both slots.")
                return

            if len(password.get()) < 4:
                showerror("WinSurfer Sign in", "There was an error while creating your account. Please make sure that your password is more than four letters long.")
                return
            
            digit = re.compile(r'\d')
            letter = re.compile(r'\w')
            special = re.compile(r'[^\w\d]')

            if re.search(digit, password.get()) == None or re.search(letter, password.get()) == None or re.search(special, password.get()) == None:
                showerror("WinSurfer Sign in", "There was an error while creating your account. Please make sure that your password has at least:\nOne alphabetical character\nOne numerical character\nOne special character")
                return
            
            new_user_data = f"{username.get()} {password.get()}    " + "15}Calibri}White}10}Terminal}White}"
            write(path, new_user_data, True)
            USER.update_user_data()
            root2.destroy()

        root.destroy()

        
        root2 = GetRoot("WinSurfer Sign-in", "200x240", "Black", None)
        root2.resizable(False, False)

        username = StringVar(root2)
        password = StringVar(root2)
        confirmed_password = StringVar(root2)

        bfont = GetFont("Terminal", 12)
        tfont = GetFont("Terminal", 10)

        GetLabel(root2, "Username", font=tfont, colour="White", bgcolour="Black").pack(pady=10, padx=10, anchor=W)
        GetEntry(root2, username, "", 14, bfont, "Black", "White", 0, 1, "White")
        GetLabel(root2, "Password", font=tfont, colour="White", bgcolour="Black").pack(pady=10, padx=10, anchor=W)
        GetEntry(root2, password, "", 14, bfont, "Black", "White", 0, 1, "White")['show'] = '*'
        GetLabel(root2, "Confirm password", font=tfont, colour="White", bgcolour="Black").pack(pady=10, padx=10, anchor=W)
        GetEntry(root2, confirmed_password, "", 14, bfont, "Black", "White", 0, 1, "White")['show'] = '*'
        GetButton(root2, "Sign in", width=9, font=GetFont("Terminal", 20, "bold"), bgColour="Black", fgColour="White", function=check_user).pack(pady=10)
        root2.mainloop()

    root = GetRoot("WinSurfer Startup", "200x200", "Black", None)
    root.resizable(False, False)
    bfont = GetFont("Terminal", 25)
    tfont = GetFont("Terminal", 10)
    GetLabel(root, "Log into your account!", font=tfont, bgcolour="Black", colour="White").pack(pady=10)
    GetButton(root, "Log in", font=bfont, width=7, bgColour="Black", fgColour="White", function=Login)
    GetLabel(root, "Create a new account!", font=tfont, bgcolour="Black", colour="White").pack(pady=10)
    GetButton(root, "Sign in", font=bfont, width=7, bgColour="Black", fgColour="White", function=Signin)
    root.mainloop()
