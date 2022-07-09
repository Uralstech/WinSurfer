"""
Author: Udayshankar R
GitHub: https://github.com/Uralstech

This encrypts and decrypts files for WinSurfer!

"""

from ShortCode.FileSystem import *
from random import *
import os

class Encryptor:
    def __init__(self):
        path = os.getcwd()
        datapath = path + r"\Data\Encryptor_key.wsef"

        self.__chars = "a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 1 2 3 4 5 6 7 8 9 0 ~ ` ! @ # $ % ^ & * ( ) _ + - = [ ] \ { } | ' ; : \" , . / < > ?"
        self.__chars = list(self.__chars.split())
        self.__chars.append(" ")
        self.__enchars = []

        if not file_exists(datapath) or file_readlines(datapath) == []:
            for i in range(len(self.__chars)):
                ival = self.__chars[i]
                ran = int(randrange(0, len(self.__chars)))
                if len(ival) == 1:
                    self.__enchars.insert(ran, str(bin(ord(ival))) + "~")
            fstr = ""
            for i in self.__enchars:
                fstr += i
            self.__enchars = fstr.split('~')
            file_override(datapath, fstr)


        fstr = file_readlines(datapath)[0]
        self.__enchars = list(fstr.split('~'))
        for i in range(len(self.__enchars)-1):
            self.__enchars[i] = chr(int(self.__enchars[i], 2))

    def encrypt_string(self, string):
        fstr = ""
        for i in string:
            if i in self.__chars:
                fstr += str(bin(ord(self.__enchars[self.__chars.index(i)])))
                fstr += "~"
            else:
                fstr += i
        return fstr
    
    def decrypt_string(self, string: str):
        fstr = ""
        for i in list(string.split('~')):
            if i != "": fstr += chr(int(i, 2))
        
        string = fstr
        fstr = ""
        
        for i in string:
            if i in self.__chars:
                fstr += self.__chars[self.__enchars.index(i)]
            else:
                fstr += i
        return fstr