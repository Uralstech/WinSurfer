from tkinter import *
from tkinter import font as f

from tkinter.messagebox import *

def GetRoot(title = "SCUI_Window", size = "512x512", colour = None, image_path = "ShortCode/InDev/Data/SCUI.png"):
    """
        Author: Udayshankar R

        Creates a Tkinter window and returns "root".
    """

    root = Tk()
    root.title(title)
    root.geometry(size)

    if image_path != None:
        if image_path != None:
            try:
                root.iconphoto(False, PhotoImage(file = image_path))
            except FileNotFoundError:
                return None

    if colour != None:
        root.config(bg= colour)
    
    return root

def GetMenu(root = None, commands = {}, subcommands = {}):
    """
        Author: Udayshankar R

        Creates a menu for the tkinter window.
    """
    
    menu = Menu(root)
    
    if commands != {} and commands != None:
        for i in commands.keys():
            menu.add_command(label=str(i), command=commands[i])
    elif subcommands != {} and subcommands != None:
        for i in subcommands.keys():
            submenu = Menu(menu, tearoff=0)
            for j in subcommands[i].keys():
                submenu.add_command(label=str(j), command=subcommands[i][j])
            menu.add_cascade(label=i, menu=submenu)

    root.config(menu=menu)
    return menu
        
def GetFont(family = "Calibri", size = 10, weight = "normal"):
    """
        Author: Udayshankar R

        Creates and returns a Tkinter.Font font. Default = "Calibri".
    """

    font = f.Font(family=family, size=size, weight=weight)
    return font

def GetLabel(
    root = None,
    text = None,
    image = None,
    width = None,
    height = None,
    font = None,
    bgcolour = None,
    colour = None):
    """
        Author: Udayshankar R

        Creates and returns a Tkinter label.
    """
    
    label = Label(root)

    if text != None:
        label = Label(root, text=text)
        if font != None:
            label['font'] = font
        if colour != None:
            label['fg'] = colour
        if bgcolour != None:
            label['bg'] = bgcolour
        if width != None:
            label['width'] = width
        if height != None:
            label['height'] = height
        label.pack()
    elif image != None:
        if width != None:
            image.config(width=width)
        if height != None:
            image.config(height=height)

        label = Label(root, image=image).pack()

    return label
    
def GetButton(
    root = None,
    text = None,
    image = None,
    function = None,
    width = None,
    height = None,
    font = None,
    bgColour = None,
    fgColour = None):
    """
        Author: Udayshankar R

        Creates and returns a tkinter button which responds to "function".
    """

    button = Button(root, command=function)

    if text != None:
        button = Button(root, text=text, command=function)
        if font != None:
            button['font'] = font
        if bgColour != None:
            button['bg'] = bgColour
        if fgColour != None:
            button['fg'] = fgColour
        if width != None:
            button['width'] = width
        if height != None:
            button['height'] = height
        button.pack()
    elif image != None:
        if width != None:
            image.config(width=width)
        if height != None:
            image.config(height=height)
        button = Button(root, image=image, command=function).pack()
        
    return button

def GetDropDown(
    root = None,
    options = None,
    width = None,
    height = None,
    font = None,
    bgColour = None,
    fgColour = None):
    """
        Author: Udayshankar R

        Creates and returns a tkinter dropdown with "options".
    """

    if type(options) == tuple:
        options = list(options)

    clicked = StringVar()
    clicked.set(options[0])

    dropdown = OptionMenu(root, clicked, *options)

    if font != None:
        dropdown['font'] = font
    if bgColour != None:
        dropdown['bg'] = bgColour
    if fgColour != None:
        dropdown['fg'] = fgColour
    if width != None:
        dropdown['width'] = width
    if height != None:
        dropdown['height'] = height

    dropdown.pack()

    return dropdown, clicked

def GetEntry(
    root = None,
    outVar = None,
    default = None, 
    width = None,
    font = None,
    bgColour = None,
    fgColour = None,
    borderSize = None,
    highlightsize = None,
    highlightcolour = None):
    """
        Author: Udayshankar R

        Creates and returns a tkinter entry.
    """
    
    entry = Entry(root, textvariable=outVar)

    if width != None:
        entry['width'] = width
    if font != None:
        entry['font'] = font
    if bgColour != None:
        entry['bg'] = bgColour
    if fgColour != None:
        entry['fg'] = fgColour
        entry['insertbackground'] = fgColour
    if borderSize != None:
        entry['bd'] = borderSize
    if highlightsize != None:
        entry['highlightthickness'] = highlightsize
    if highlightcolour != None:
        entry.config(highlightcolor=highlightcolour)
    if default != None:
        entry.insert(END, default)
    entry.pack()

    return entry