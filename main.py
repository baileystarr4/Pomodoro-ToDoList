#TO DO 
#  Fix UI
#      # Make Buttons Cuter
#      # Move Everything
#  Windows Pop Ups
#  Make into a Windows App
from tkinter import *
import math
import pygame

# ---------------------------- GLOBALS AND CONSTANTS ------------------------------- # 
DARK_COLOR = "#272829"
LIGHT_COLOR = "#D8D9DA"
FONT_NAME = "Courier"
work_min = 60
snooze_min = 10
reps = 0
timer = None

# ---------------------------- TIMER ------------------------------- # 
def start_timer():
    global reps
    reps += 1

    entry.unbind('<Return>')
    question_label.place_forget()
    entry.place_forget()
    
    if reps % 2 == 0:
        timer_label.config(text="STRETCH")
        canvas.place_forget()
        play()
        work_button.config(command=clicked_work)
        work_button.place(relx=0.3, rely=0.6, anchor='center')
        button.config(text="Snooze", command=clicked_snooze)
        button.place(relx=0.7, rely=0.6, anchor='center')
    else:
        button.config(text="Reset", command=clicked_reset_button)
        button.place(relx=0.5,rely=0.7, anchor='center')
        work_sec = work_min * 60
        count_down(work_sec)
        timer_label.config(text="Work")   

def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_min < 10:
        count_min=f"0{count_min}"
    if count_sec < 10:
        count_sec=f"0{count_sec}"
    canvas.place(relx=0.5,rely=0.475, anchor='center')
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()

# ---------------------------- BUTTON COMMANDS ------------------------------- # 
def clicked_reset_button():
    window.after_cancel(timer)
    canvas.place_forget()
    button.place_forget()
    timer_label.config(text="Stretch Timer")
    default_button.place(relx=0.4,rely=0.6, anchor='center')
    custom_button.place(relx=0.6,rely=0.6, anchor='center')

    global reps
    reps = 0

def clicked_custom_button():
    custom_button.place_forget()
    default_button.place_forget()
    question_label.config(text="How long would you like to work? \n Enter in minutes")
    question_label.place(relx=0.5,rely=0.425, anchor='center')

    entry.place(relx=0.5,rely=0.55, anchor='center')
    entry.focus()
    entry.delete(0, END)
    entry.insert(0, "30")
    entry.bind('<Return>', (lambda event: save_time_work()))

    button.config(command=save_time_work)
    button.place(relx=0.5,rely=0.7, anchor='center')

def clicked_default_button():
    custom_button.place_forget()
    default_button.place_forget()
    start_timer()

def clicked_snooze():
    pygame.mixer.music.stop()
    button.place_forget()
    work_button.config(command=clicked_work_from_snooze)
    work_button.place(relx=0.5, rely=0.7, anchor='center')
    global reps
    reps -= 1
    snooze_sec = snooze_min * 60
    count_down(snooze_sec)

def clicked_work_from_snooze():
    global reps
    reps += 1
    clicked_work()

def clicked_work():
    pygame.mixer.music.stop()
    work_button.place_forget()
    window.after_cancel(timer)
    start_timer()
# ---------------------------- SAVE USER INPUT ------------------------------- # 
def save_time_work():
    input = int(entry.get())
    global work_min
    work_min = input

    button.config(command=save_time_snooze)
    entry.bind('<Return>', (lambda event: save_time_snooze()))
    question_label.config(text="How long would you like to snooze?\n Enter in minutes")
    entry.delete(0, END)
    entry.insert(0, "5")

def save_time_snooze():
    input = int(entry.get())
    global snooze_min
    snooze_min = input
    start_timer()

# ---------------------------- PLAY ALARM ------------------------------- # 
def play():
    pygame.mixer.music.load("219244__zyrytsounds__alarm-clock-short.wav")
    pygame.mixer.music.play(loops=1)

# ---------------------------- UI ------------------------------- # 
window = Tk()
window.title("Stretch Timer")
window.config(bg=DARK_COLOR)
window.geometry('600x500')

timer_label = Label(text="Stretch Timer", font=(FONT_NAME, 50, "bold"), fg=LIGHT_COLOR, bg=DARK_COLOR)
timer_label.place(relx=0.5,rely=0.25, anchor='center')
default_button = Button(text="Default", command=clicked_default_button, bg=LIGHT_COLOR, fg=DARK_COLOR, font=(FONT_NAME, 15,"bold"), height=1, width=8)
default_button.place(relx=0.3,rely=0.6, anchor='center')
custom_button = Button(text="Custom", command=clicked_custom_button, bg=LIGHT_COLOR, fg=DARK_COLOR, font=(FONT_NAME, 15, "bold"), height=1, width=8)
custom_button.place(relx=0.7,rely=0.6, anchor='center')

question_label = Label(font=(FONT_NAME, 18, "bold"), fg=LIGHT_COLOR, bg=DARK_COLOR)
entry = Entry(window, width=10, font=(FONT_NAME, 15,"bold"), justify= CENTER)
button = Button(text="Save", command=save_time_work, bg=LIGHT_COLOR, fg=DARK_COLOR, font=(FONT_NAME, 15, "bold"), height=1, width=8)
canvas = Canvas(width=200, height=100, bg=DARK_COLOR, highlightthickness=0)
timer_text = canvas.create_text(100, 50, text="00:00", fill = LIGHT_COLOR, font=(FONT_NAME, 40, "bold"))
work_button = Button(text="Work", command=clicked_work, bg=LIGHT_COLOR, fg=DARK_COLOR, font=(FONT_NAME, 15, "bold"), height=1, width=8)
pygame.mixer.init()

window.mainloop()