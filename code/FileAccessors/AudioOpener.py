"""
Author: Udayshankar R
GitHub: https://github.com/Uralstech

Helps WinSurfer with audio files!

"""

from time import strftime, gmtime
from ShortCode.InDev.UI import *
from mutagen.wave import WAVE
from mutagen.mp3 import MP3
from pygame import mixer
import os

def open_file(root, current_path:str):
    title = os.path.basename(current_path)

    root2 = Toplevel(root, bg="Black")
    root2.title(title)
    root2.geometry("350x250")
    root2.resizable(False, False)
    
    global paused
    paused = False

    volumes = [0]
    for i in range(1, 101):
        volumes.append(volumes[i-1]+1/100)

    music = None
    music_length = 0
    formatted_music_length = ""
    file_type = os.path.splitext(current_path)[1]
    if file_type == ".mp3":
        music = MP3(current_path)
    elif file_type == ".wav":
        music = WAVE(current_path)
    if music != None:
        music_length = music.info.length
        formatted_music_length = strftime('%H:%M:%S', gmtime(music_length))

    def get_time():
        if not paused and not mixer.music.get_busy():
            if music != None:
                timeline_scale['state'] = 'normal'
                timeline_scale.set(0)
                if file_type == ".wav": timeline_scale['state'] = 'disabled'
            b['text'] = "Play"
            status_bar['text'] = "00:00:00" + (('/' + formatted_music_length) if music != None else "")

        if mixer.music.get_busy():
            if music != None: current_time = timeline_scale.get() + 1
            else: current_time = int(mixer.music.get_pos() / 1000)

            formatted_current_time = strftime('%H:%M:%S', gmtime(current_time))
            status_bar['text'] = formatted_current_time + (('/' + formatted_music_length) if music != None else "")
            if music != None:
                timeline_scale['state'] = 'normal'
                timeline_scale.set(current_time)
                if file_type == ".wav": timeline_scale['state'] = 'disabled'
        
        root2.after(1000, get_time)

    def toggle_pause(is_paused):
        global paused
        paused = is_paused

        if not paused and not mixer.music.get_busy():
            mixer.music.play(loops=0)
            b['text'] = "Pause"
            return

        if is_paused:
            mixer.music.unpause()
            b['text'] = "Pause"
            paused = False
        else:
            mixer.music.pause()
            b['text'] = "Play"
            paused = True

    def restart():
        if mixer.music.get_busy() and not paused:
            if music != None:
                timeline_scale['state'] = 'normal'
                timeline_scale.set(0)
                if file_type == ".wav": timeline_scale['state'] = 'disabled'
            mixer.music.play(loops=0, start=0)

    def close_window():
        mixer.music.stop()
        mixer.music.unload()
        root2.destroy()
    
    def set_volume(v=None):
        mixer.music.set_volume(volumes[volume.get()])

    def set_time(v=None, time=0):
        if file_type == ".mp3":
            if time != 0:
                mixer.music.set_pos(timeline_scale.get() + time)
                timeline_scale.set(timeline_scale.get() + time)
            else:
                mixer.music.set_pos(timeline_scale.get())

    mixer.init()
    mixer.music.load(current_path)

    tfont = GetFont("Terminal", 15)
    tfont2 = GetFont("Terminal", 10)
    b = GetButton(root2, "Play", width=32, font=tfont, bgColour="Black", fgColour="White", function=lambda:toggle_pause(paused)) ; b.pack(pady=5)
    GetButton(root2, "Restart", width=32, font=tfont, bgColour="Black", fgColour="White", function=restart)
    GetLabel(root2, "volume", font=tfont2, bgcolour="Black", colour="White").pack(anchor=W, padx=10, pady=5)
    volume = Scale(root2, bg="Black", troughcolor="Black", font=tfont, fg="White", orient=HORIZONTAL, from_=0, to=100, command=set_volume) ; volume.pack(fill="x", expand=1, padx=10, anchor=N) ; volume.set(100)
    GetLabel(root2, "timeline", font=tfont2, bgcolour="Black", colour="White").pack(anchor=W, padx=10, pady=5)
    status_bar = GetLabel(root2, "00:00:00/00:00:00", font=tfont2, bgcolour="Black", colour="White") ; status_bar.pack(padx=10, anchor=W, side=BOTTOM)
    
    if music != None:
        timeline_scale = Scale(root2, bg="Black", troughcolor="Black", font=tfont, fg="White", orient=HORIZONTAL, from_=0, to=music_length)
        timeline_scale.pack(fill="x", expand=1, padx=10, pady=5, side=BOTTOM)
        timeline_scale.bind("<ButtonRelease-1>", set_time)
        timeline_scale['state'] = 'disabled'
    else:
        GetLabel(root2, "Timeline not supported", font = tfont, bgcolour="Black", colour="White").pack(pady=5, side=BOTTOM)

    get_time()
    root2.bind('<a>', lambda x: set_time(time=-5))
    root2.bind('<d>', lambda x: set_time(time=5))
    root2.bind('<p>', lambda x: toggle_pause(paused))
    root2.protocol("WM_DELETE_WINDOW", close_window)
    root2.mainloop()