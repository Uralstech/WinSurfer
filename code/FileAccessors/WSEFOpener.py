"""
Author: Udayshankar R
GitHub: https://github.com/Uralstech

Helps WinSurfer with WSEF (WinSurfer Encrypted File) files!

"""

from ShortCode.FileSystem import *
from Encryptor import Encryptor
import os

local_encryptor = Encryptor()

def write(path, data, append=False, split_by=" ", is_formatted=False):
    """
    Author: Udayshankar R
    GitHub: https://github.com/Uralstech

    Writes given data to a file.

    path: (str) Path to file.
    data: (list/tuple/str) Data to be written.
    append: (bool) If True, appends to the file. Otherwise, overrides data in file.
    split_by: (str) The string for the split function used when formatting (str) data.
    is_formatted: (bool) Set to True if data is already formatted (i.e has lines defined).

    NOTE: If file does not exist, this will create it.
    """
    
    if os.path.splitext(path)[1] != ".wsef":
        print("WSEFOpener is optimized for opening .wsef files. Please use TextOpener or ShortCode.FileSystem.")
        return None
    
    if is_formatted: split_by = '\n'

    fstr = ""
    if type(data) == list or type(data) == tuple:
        for i in data: fstr += local_encryptor.encrypt_string(str(i)) + '\n'
        data = fstr
    elif type(data) == str:
        data = list(data.split(split_by))
        for i in data: fstr += local_encryptor.encrypt_string(str(i)) + '\n'
        data = fstr
    
    if append:
        file_append(path, data)
    else:
        file_override(path, data)

def read(path, lines_to_read=-1, format_string=False):
    """
    Author: Udayshankar R
    GitHub: https://github.com/Uralstech

    Reads and returns data from a file.

    path: (str) Path to file.
    lines_to_read: (int) Number of lines to read from file. Default: -1 (reads all lines).
    format_string: (bool) Set to True if data should be formatted (i.e have defined lines).

    """

    if os.path.splitext(path)[1] != ".wsef":
        print("WSEFOpener is optimized for opening .wsef files. Please use TextOpener or ShortCode.FileSystem.")
        return None

    if file_exists(path):
        data = file_readlines(path)

        for i in range(len(data)):
            s = ""
            for j in data[i]:
                if j != '\n':
                    s += j
            data[i] = s

        for i in range(len(data)):
            data[i] = local_encryptor.decrypt_string(data[i])
            if format_string: data[i] += "\n"

        if lines_to_read >= 0:
            lines = []
            for i in range(lines_to_read + 1):
                lines.append(data[i])
            return lines
        else:
            return data
    else:
        print(f"File at {path} doesn't exist.")