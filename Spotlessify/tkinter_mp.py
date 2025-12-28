from tkinter import filedialog
from tkinter import *
import pygame
import os
import pytubefix
from pytubefix import YouTube
from pytubefix.cli import on_progress
import pywhatkit
import requests
import pafy
from moviepy.editor import VideoFileClip

root = Tk()
root.title("Spotlessify")
root.geometry("600x430")

pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song = " "
paused = False

def search_music():
    search_query = search.get() 
    for song in songlist.get(0, END):
        if search_query.lower() in song.lower():
            label = Label(root, text = "Already Satisfied!")
            label.pack()
        else:
            y = pywhatkit.playonyt(search_query, open_video = False)
            url = requests.get(y).url
            requested_song = YouTube(url, on_progress_callback = on_progress)
            print(requested_song.title)
            ys = requested_song.streams.filter(only_audio = True).first()
            out_file = ys.download(output_path = "C:\\Users\\ronak\\OneDrive\\Desktop\\Musi")
            v = moviepy.VideoFileClip(out_file)
            audio = v.audio
            audio.write_audiofile(output_file)
            

search = Entry(root, width = 50)
search.pack()
search_btn = Button(root, text="Search", command=search_music)
search_btn.pack()
search_query = search.get()

def load_music():
    global current_song
    root.directory = "C:\\Users\\ronak\\OneDrive\\Desktop\\Musi"
    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == ".mp3":
            songs.append(song)

    for song in songs:
        songlist.insert("end", song)

    songlist.selection_set(0)
    current_song = songs[songlist.curselection()[0]]

def play_music():
    global current_song, paused

    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_music():
    global current_song, paused

    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song) + 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass
    
def prev():
    global current_song, paused

    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song) - 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label="Music", command = load_music)
menubar.add_cascade(label = "Music", menu = organise_menu)

songlist = Listbox(root, bg="black", fg="white", width=100, height=15)
songlist.pack()

play_btn_img = PhotoImage(file="C:\\Users\\ronak\\OneDrive\\Desktop\\Spotlessify\\play.png")
pause_btn_img = PhotoImage(file="C:\\Users\\ronak\\OneDrive\\Desktop\\Spotlessify\\pause.png")
next_btn_img = PhotoImage(file="C:\\Users\\ronak\\OneDrive\\Desktop\\Spotlessify\\next.png")
prev_btn_img = PhotoImage(file="C:\\Users\\ronak\\OneDrive\\Desktop\\Spotlessify\\previous.png")

control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame, image = play_btn_img, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image = pause_btn_img, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image = next_btn_img, borderwidth=0, command=next_music)
prev_btn = Button(control_frame, image = prev_btn_img, borderwidth=0, command=prev)

play_btn.grid(row=0, column=1, padx = 7, pady = 10)
pause_btn.grid(row=0, column=2, padx = 7, pady = 10)
next_btn.grid(row=0, column=3, padx = 7, pady = 10)
prev_btn.grid(row=0, column=0, padx = 7, pady = 10)

root.mainloop()
