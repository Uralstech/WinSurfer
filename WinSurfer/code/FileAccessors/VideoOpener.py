"""
Author: Udayshankar R
GitHub: https://github.com/Uralstech

Helps WinSurfer with video files!

"""

from time import strftime, gmtime
from ShortCode.InDev.UI import *
from pyvidplayer import Video
from pygame import display
import os

def open_file(root, current_path:str):
    title = os.path.basename(current_path)

    root2 = Toplevel(root, bg="Black")
    root2.title(title)
    root2.geometry("350x215")
    root2.resizable(False, False)

    global paused
    paused = False

    global called
    called = False

    volumes = [0]
    for i in range(1, 101):
        volumes.append(volumes[i-1]+1/100)

    def get_time(end=False):
        duration = videoplayer.get_file_data()["duration"]
        if timeline_scale['to'] != duration:
            timeline_scale['to'] = duration
        
        current_time = int(videoplayer.get_playback_data()["time"])
        formatted_current_time = strftime('%H:%M:%S', gmtime(current_time))
        formatted_duration = strftime('%H:%M:%S', gmtime(duration))

        status_bar['text'] = formatted_current_time + "/" + formatted_duration
        timeline_scale.set(current_time)

        if end and not paused:
            toggle_pause(paused)

        if videoplayer.get_playback_data()["time"] > duration - 0.3 and not end: root2.after(100, lambda:get_time(True))
        else: root2.after(1000, get_time)

    def update():
        global called

        videoplayer.draw(screen, (0, 0))
        display.update()
        if not called: get_time() ; called = True
        root2.after(16, update)

    def toggle_pause(is_paused):
        global paused
        paused = is_paused

        videoplayer.toggle_pause()
        paused = not paused

        if paused: b['text'] = "Play"
        else: b['text'] = "Paused"

    def close_window():
        videoplayer.close()
        display.quit()
        root2.destroy()

    def set_time(v=None, time=None):
        if time == None: videoplayer.seek(int(timeline_scale.get() - videoplayer.get_playback_data()["time"]))
        else: videoplayer.seek(time)

    def set_volume(v=None): videoplayer.set_volume(volumes[volume.get()])

    display.init()
    videoplayer = Video(current_path);
    video_size = videoplayer.get_file_data()['original size']
    videoplayer.set_size(video_size)

    display.set_caption(title)
    screen = display.set_mode(video_size)

    tfont = GetFont("Terminal", 15)
    tfont2 = GetFont("Terminal", 10)
    b = GetButton(root2, "Pause", width=32, font=tfont, bgColour="Black", fgColour="White", function=lambda:toggle_pause(paused)) ; b.pack(pady=5)
    GetLabel(root2, "volume", font=tfont2, bgcolour="Black", colour="White").pack(anchor=W, padx=10)
    volume = Scale(root2, bg="Black", troughcolor="Black", font=tfont, fg="White", orient=HORIZONTAL, from_=0, to=100, command=set_volume) ; volume.pack(fill="x", expand=1, padx=10, pady=5, anchor=N) ; volume.set(100)
    GetLabel(root2, "timeline", font=tfont2, bgcolour="Black", colour="White").pack(anchor=W, padx=10)
    status_bar = GetLabel(root2, "00:00:00/00:00:00", font=tfont2, bgcolour="Black", colour="White") ; status_bar.pack(padx=10, pady=5, anchor=W, side=BOTTOM)
    timeline_scale = Scale(root2, bg="Black", troughcolor="Black", font=tfont, fg="White", orient=HORIZONTAL, from_=0, to=1) ; timeline_scale.pack(fill="x", expand=1, padx=10, pady=5, side=BOTTOM)
    timeline_scale.bind("<ButtonRelease-1>", set_time)
    update()

    root2.bind('<a>', lambda x: set_time(time=-5))
    root2.bind('<d>', lambda x: set_time(time=5))
    root2.bind('<p>', lambda x: toggle_pause(paused))
    root2.protocol("WM_DELETE_WINDOW", close_window)
    root2.mainloop()