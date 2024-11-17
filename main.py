from pytubefix import YouTube
from PIL import ImageTk, Image
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
import requests
import os


window = ttk.Window(size=(700, 700), title="jamu's Youtube Tool", themename="darkly")
ico = Image.open("icon.png")
img = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, img)

# variables
url = ""
img = ""
option_text = ttk.StringVar()
options = ["Type","Video & Audio","Audio"]
video_info = ttk.StringVar()
yt = ""

# functions
def close():
    try:
        os.remove("thumbnail.jpg")
    except:
        print("file not found")
    window.destroy()

def find_video():
    global url
    global img
    global yt
    success_label.config(text="")
    url = input_box.get("1.0", "end-1c")
    print(url)
    try:
        yt = YouTube(url)
        img_data = requests.get(yt.thumbnail_url).content
        with open("thumbnail.jpg", "wb") as file:
            file.write(img_data)

        image_raw = Image.open("thumbnail.jpg")
        image_resized = image_raw.resize((400, 300))
        img = ImageTk.PhotoImage(image_resized)
        img_label.config(image=img)

        video_info.set(yt.title)

        options_menu.pack(pady=10)
        
        download_button.pack()
    except:
        print("invalid url")
        messagebox.showwarning("Warning", "INVALID URL: "+url)

def download():
    global yt
    res = []
    for stream in yt.streams:
        res.append(stream.resolution) 
    file_path = filedialog.askdirectory()
    if file_path != "":
        selection = option_text.get()
        if selection == "Audio":
            try:
                mp3 = yt.streams.get_audio_only()
                mp3.download(mp3=True, output_path=file_path)
                success_label.config(text="Download Complete")
            except:
                success_label.config(text="Download Failed")
        elif selection == "Video & Audio":
            try:
                video = yt.streams.filter(res=res[1])
                video.first().download(output_path=file_path)
                success_label.config(text="Download Complete")
                mp3 = yt.streams.get_audio_only()
                mp3.download(mp3=True, output_path=file_path)
            except:
                success_label.config(text="Download Failed")

# layout
title_label = ttk.Label(window, text="Jamu's Youtube Tool", font="Consolas 30 bold", style="danger")
title_label.pack()

url_label = ttk.Label(window, text="URL", font="Consolas 20")
url_label.pack(pady=10)

input_box = ttk.Text(window, width=40, height=1)
input_box.pack()

find_button = ttk.Button(window, text="Find Video", command=find_video, style="danger")
find_button.pack(pady=10)

img_label = ttk.Label(window)
img_label.pack()

info_frame = ttk.Frame(window)
info_frame.pack()

info_label = ttk.Label(info_frame, textvariable=video_info, font="Consolas 15 bold")
info_label.grid(row=0, column=0)

success_label = ttk.Label(window, style="success", font="Consolas 10")
success_label.pack(pady=10)

options_menu = ttk.OptionMenu(window, option_text, *options, style="secondary")

download_button = ttk.Button(window, text="Download", width=50, style="danger", command=download)

window.protocol("WM_DELETE_WINDOW", close)

window.mainloop()