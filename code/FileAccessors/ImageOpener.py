"""
Author: Udayshankar R
GitHub: https://github.com/Uralstech

Helps WinSurfer with image files!

"""

from ShrtCde.InDev.UI import *
from PIL import ImageTk, Image
import os

def open_file(root, current_path:str):
    root2 = Toplevel(root, bg="Black")
    title = os.path.basename(current_path)

    root2.title(title)
    root2.resizable(False, False)

    def resize_image(v=None):
        size = size_scale.get()
        image = Image.open(current_path)

        if size < 0:
            size = int(str(size)[1])
            size = (ogx // (size + 1), ogy // (size + 1))
        elif size > 0:
            size = (ogx * (size + 1), ogy * (size + 1))
        else:
            size = (ogx, ogy)

        if size[0] < 200 or size[1] < 100:
            showerror("WinSurfer ImageViewer", "IMAGE SIZE TOO SMALL")
            return
        
        image = image.resize(size)
        root2.geometry(str(size[0] + 5) + 'x' + str(size[1] + 5))

        imagetk = ImageTk.PhotoImage(image)
        display.config(image=imagetk)
        display.image = imagetk
    
    def close_window():
        root2.destroy()
        root3.destroy()

    image = Image.open(current_path)
    imagetk = ImageTk.PhotoImage(image)
    ogx = image.width
    ogy = image.height

    root2.geometry(str(ogx + 5) + 'x' + str(ogy + 5))
    display = Label(root2, bg="Black", image=imagetk)
    display.pack(anchor=CENTER)
    display.image = imagetk

    root3 = Toplevel(root, bg="Black")
    root3.title(title + " zoom")
    root3.geometry("300x60")
    root3.resizable(False, False)

    size_scale = Scale(root3, bg="Black", troughcolor="Black", font=GetFont("Terminal", 15), fg="White", orient=HORIZONTAL, from_=-3, to=3, command=resize_image) ; size_scale.pack(fill="x", expand=1, padx=5, pady=5) ; size_scale.set(0)

    root2.bind('<a>', lambda x: size_scale.set(size_scale.get() - 1))
    root2.bind('<d>', lambda x: size_scale.set(size_scale.get() + 1))
    root3.bind('<a>', lambda x: size_scale.set(size_scale.get() - 1))
    root3.bind('<d>', lambda x: size_scale.set(size_scale.get() + 1))
    root2.protocol("WM_DELETE_WINDOW", close_window)
    root3.protocol("WM_DELETE_WINDOW", close_window)
    root3.mainloop()
    root2.mainloop()