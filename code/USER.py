"""
Author: Udayshankar R
GitHub: https://github.com/Uralstech

The class that contains info about the USER!

"""

from FileAccessors.WSEFOpener import write, read
from Encryptor import Encryptor
import os

path = os.getcwd() + r"\Data\User_data.wsef"

class USER:
    all = []
    logged_user = None
    local_encryptor = Encryptor()

    def __init__(self, username:str, password:str, searches:list, font:str):
        self.username = username
        self.password = USER.local_encryptor.encrypt_string(password)
        self.searches = searches

        self.font = font
        font = list(font.split('}'))
        font[0] = int(font[0])
        font[3] = int(font[3])
        self.formatted_font = font

        USER.all.append(self)
    
    @classmethod
    def update_user_data(cls):
        cls.all = []
        data = read(path)

        user = []
        for i in range(len(data)):
            user.append(data[i])

            if len(user) >= 6:
                u = USER(user[0], user[1], [user[2], user[3], user[4]], user[5])
                if cls.logged_user != None:
                    if u.username == cls.logged_user.username:
                        cls.logged_user = u
                user = []
        
    def write_searches(self, new_searches:list):
        for i in new_searches:
            if " " in i:
                new_search = ""
                for j in i:
                    if j != " ": new_search += j
                    else: new_search += "|"
                new_searches[new_searches.index(i)] = new_search

        users = USER.all
        data = ""
        for i in users:
            if i.username == self.username:
                s = ""
                s += self.username + "\n"
                s += USER.local_encryptor.decrypt_string(self.password) + "\n"
                s += new_searches[0] + "\n"
                s += new_searches[1] + "\n"
                s += new_searches[2] + "\n"
                s += self.font
                data += s
            else:
                s = ""
                s += i.username + "\n"
                s += USER.local_encryptor.decrypt_string(i.password) + "\n"
                s += i.searches[0] + "\n"
                s += i.searches[1] + "\n"
                s += i.searches[2] + "\n"
                s += i.font
                data += s
            
            if USER.all.index(i) < len(USER.all) - 1:
                data += "\n"
        write(path, data)
        USER.update_user_data()
    
    def write_font(self, font:list):
        users = USER.all
        data = ""

        fstr = ""
        for i in font:
            fstr += str(i) + "}"
        font = fstr

        for i in users:
            if i.username == self.username:
                s = ""
                s += self.username + "\n"
                s += USER.local_encryptor.decrypt_string(self.password) + "\n"
                s += self.searches[0] + "\n"
                s += self.searches[1] + "\n"
                s += self.searches[2] + "\n"
                s += font
                data += s
            else:
                s = ""
                s += i.username + "\n"
                s += USER.local_encryptor.decrypt_string(i.password) + "\n"
                s += i.searches[0] + "\n"
                s += i.searches[1] + "\n"
                s += i.searches[2] + "\n"
                s += i.font
                data += s
            
            if USER.all.index(i) < len(USER.all) - 1:
                data += "\n"
        write(path, data, is_formatted=True)
        USER.update_user_data()
    
    def __repr__(self):
        return f"\nUser {self.username}:\nPassword: {self.password}\nSearches: {self.searches}\nFont prefs (formatted): {self.formatted_font}\nFont prefs (raw): {self.font}\n"