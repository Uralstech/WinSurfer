"""
Author: Udayshankar R
GitHub: https://github.com/Uralstech

The main code for WinSurfer!

"""

from FileAccessors import ImageOpener, AudioOpener, VideoOpener, TextOpener
from FileAccessors.WSEFOpener import read, write
from ShortCode.FileSystem import *
from ShortCode.InDev.UI import *
from tkinter import filedialog
from Encryptor import *
from USER import USER
import Login
import os

cwd = os.getcwd()
path = cwd + r"\Data\User_data.wsef"
base_path = r"C:\Users" + "\\" + os.getlogin()
if not file_exists(path) or file_readlines(path) == []:
    write(path, "DEFAULTUSER DefUsr123#    15}Calibri}White}10}Terminal}White}")
    showinfo("THANK YOU FOR DOWNLOADING WINSURFER!", "WinSurfer is a command-line-style UI file explorer. These are the supported files!\n\nTEXT: .txt, .docx(buggy, not recommended), .wsef(custom), and any text file\nIMAGE: .png, .jpg, .gif, .tiff, .ico and a lot more!\nAUDIO: .mp3, .wav(partially), .ogg(partially)\nVIDEO: .mp4\nPYTHON: .py (WITH BUILT-IN IDE)\n\nSHORTCUTS (Main):\nEnter: Open file at given path\nCtrl+O: Open file using Windows Explorer\nCtrl+N: Open file creation dialog\n\nSHORTCUTS (Image viewer)\nA: Decrease size of image by one unit\nD: Increase size of image by one unit\n\nSHORTCUTS (Videoplayer):\nP: Toggle pause\nA: Skip -5 seconds\nD: Skip +5 seconds\n\nSHORTCUTS (Text editor):\nCtrl+S: Save\n(pyIDE) F5: Run file\n(pyIDE) Ctrl+C: Clear console\n\nAgain, thanks a lot for downloading this. Feel free to report any bugs at https://github.com/Uralstech")

USER.update_user_data()
while USER.logged_user == None:
    Login.Start()

global used
used = 0
def search_file(v=None):
    global used
    used = used

    current_path = entry.get()
    existing_searches = USER.logged_user.searches

    def set_button(b):
        b['text'] = current_path
        b.config(command=lambda:set_entry_and_search(current_path))
        existing_searches[buttons.index(b)] = current_path
        USER.logged_user.write_searches(existing_searches)

    if file_exists(current_path):
        buttons = [b1, b2, b3]
        text = [b1['text'], b2['text'], b3['text']]
        all_used = True
        for i in buttons:
            if current_path in text:
                all_used = False
                break
            if i['text'] == "...":
                set_button(i)
                all_used = False
                break
        if all_used:
            set_button(buttons[used])
            used += 1
            if used > 2: used = 0
        
        file_type = os.path.splitext(current_path)[1]
        supported_images = [".png", ".jpg", ".jpeg", ".gif", ".tiff", ".ico", ".icns", ".im", ".eps", ".dib", ".dds", ".bmp", ".blp", ".msp", ".pcx", ".ppm", ".pgm", ".pnm", ".pbm", ".sgi", ".tga"]
        supported_music = [".mp3", ".wav", ".ogg"]

        if file_type in supported_images:
            ImageOpener.open_file(root, current_path)
        elif file_type in supported_music:
            AudioOpener.open_file(root, current_path)
        elif file_type == ".mp4":
            VideoOpener.open_file(root, current_path)
        else:
            TextOpener.open_file(root, current_path, cwd + "\Data\\")
    else:
        showerror("WinSurfer", f"File at {current_path} doesn't exist!")
def set_entry_and_search(current_path):
    entry.set(current_path)
    search_file()
def open_and_search_file(v=None):
    current_path = filedialog.askopenfilename(title="Select file to open", initialdir=base_path, filetypes=(
        ('Text file', '.txt'),
        ('Text Document (Buggy, not recommended)', '.docx'),
        ('WinSurfer Encrypted file', '.wsef'),
        ('Image (PNG)', '.png'),
        ('Image (JPG, JPEG)', '.jpg .jpeg'),
        ('Audio (MP3)', '.mp3'),
        ('Audio (WAVE)', '.wav'),
        ('Audio (OGG)', '.ogg'),
        ('Video (MP4)', '.mp4'),
        ('Python (Using built-in IDE)', '.py'),
        ('All files', '*.*')))
    new_path = ""
    for i in current_path:
        if i != "/": new_path += i
        else: new_path += '\\'
    current_path = new_path
    set_entry_and_search(current_path)
def create_file(v=None):
    root2 = Toplevel(root, bg="Black")
    root2.geometry("512x110")
    root2.title("WinSurfer Creator")
    root2.resizable(False, False)

    def open_explorer():
        types = (('Text file', '*.txt'),
                 ('Text Document (Buggy, not recommended)', '*.docx'),
                 ('WinSurfer Encrypted file', '*.wsef'),
                 ('Python file', '*.py'),
                 ('All files', '*.*'))

        new_path = filedialog.asksaveasfilename(title="Create file", initialdir=base_path, confirmoverwrite=False, filetypes=types, defaultextension=types)
        edpath = ""
        for i in new_path:
            if i != "/": edpath += i
            else: edpath += '\\'
        new_path = edpath
        current_path.set(new_path)
    def create():
        if not current_path.get().startswith("C:\\") or file_exists(current_path.get()):
            showerror("WinSurfer Creator", f"There was an error while creating the file at {current_path.get()}. The path is empty or the file already exists.")
            return
        open(current_path.get(), 'w').close()
        set_entry_and_search(current_path.get())
        root2.destroy()
        
    current_path = StringVar(root2)
    efont = GetFont("Terminal", 20)

    GetMenu(root2, {"Open explorer" : open_explorer})
    GetEntry(root2, current_path, "Enter file path...", 30, efont, "Black", "White", 0, 1, "White").pack(pady=15)
    GetButton(root2, "Create", font=efont, width=30, bgColour="Black", fgColour="White", function=create)
    root2.mainloop()

root = GetRoot("WinSurfer", "512x455", "Black", None)
root.resizable(False, False)

entry = StringVar(root)

efont = GetFont("Terminal", 20)

GetMenu(root, {"Open explorer" : open_and_search_file, "Create file" : create_file})
GetEntry(root, entry, "Enter file path...", 30, efont, "Black", "White", 0, 1, "White").pack(pady=15)
GetButton(root, "Search", font=efont, width=30, bgColour="Black", fgColour="White", function=search_file)
GetButton(root, base_path + r"\Desktop", font=efont, width=30, bgColour="Black", fgColour="White", function=lambda:entry.set(base_path + r"\Desktop")).pack(pady=15)
GetButton(root, base_path + r"\Downloads", font=efont, width=30, bgColour="Black", fgColour="White", function=lambda:entry.set(base_path + r"\Downloads"))
GetButton(root, base_path + r"\Pictures", font=efont, width=30, bgColour="Black", fgColour="White", function=lambda:entry.set(base_path + r"\Pictures")).pack(pady=15)
b1 = GetButton(root, "...", font=efont, width=30, bgColour="Black", fgColour="White", function=lambda:entry.set("..."))
b2 = GetButton(root, "...", font=efont, width=30, bgColour="Black", fgColour="White", function=lambda:entry.set("..."))
b2.pack(pady=15)
b3 = GetButton(root, "...", font=efont, width=30, bgColour="Black", fgColour="White", function=lambda:entry.set("..."))

searches = USER.logged_user.searches
for i in searches:
    new_search = ""
    for j in i:
        if j != "|": new_search += j
        else: new_search += " "
    searches[searches.index(i)] = new_search

if file_exists(searches[0]): b1['text'] = searches[0] ; b1.config(command=lambda:set_entry_and_search(searches[0]))
if file_exists(searches[1]): b2['text'] = searches[1] ; b2.config(command=lambda:set_entry_and_search(searches[1]))
if file_exists(searches[2]): b3['text'] = searches[2] ; b3.config(command=lambda:set_entry_and_search(searches[2]))

root.bind('<Return>', search_file)
root.bind('<Control-o>', open_and_search_file)
root.bind('<Control-n>', create_file)
root.mainloop()