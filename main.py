#TO DO 
#  Windows Pop Ups
#  Make into a Windows App

from tkinter import *
from tkinter import messagebox
import math
import pygame
from winotify import Notification

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

    # Remove unnecessary widgets from the screen
    entry.unbind('<Return>')
    question_label.place_forget()
    entry.place_forget()
    
    # Is it time to stretch?
    if reps % 2 == 0:
        timer_label.config(text="STRETCH")
        canvas.place_forget()
        play()
        work_button.config(command=clicked_work)
        work_button.place(relx=0.3, rely=0.6, anchor='center')
        button.config(text="Snooze", command=clicked_snooze)
        button.place(relx=0.7, rely=0.6, anchor='center')
        toast.show()

    # If not, it's time to work
    else:
        timer_label.config(text="Work")
        button.config(text="Reset", command=clicked_reset_button)
        button.place(relx=0.5,rely=0.7, anchor='center')
        work_sec = work_min * 60
        count_down(work_sec)    

def count_down(count):
    # Count down mechanism
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_min < 10:
        count_min=f"0{count_min}"
    if count_sec < 10:
        count_sec=f"0{count_sec}"

    # Update timer on screen
    canvas.place(relx=0.5,rely=0.475, anchor='center')
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    # If the timer has not ended, continue counting down
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    # Otherwise, stop counting and start the timer again    
    else:
        start_timer()

# ---------------------------- BUTTON COMMANDS ------------------------------- # 
def clicked_custom_button():
    # Remove unnecessary widgets from the screen
    custom_button.place_forget()
    default_button.place_forget()

    # Ask for user input
    question_label.config(text="How long would you like to work? \n Enter in minutes")
    question_label.place(relx=0.5,rely=0.425, anchor='center')

    # Add entry and save button widgets to the screen
    entry.place(relx=0.5,rely=0.55, anchor='center')
    entry.focus()
    entry.delete(0, END)
    entry.insert(0, "30")
    entry.bind('<Return>', (lambda event: save_time_work()))

    button.config(command=save_time_work)
    button.place(relx=0.5,rely=0.7, anchor='center')

def clicked_default_button():
    # Remove unnecessary widgets from the screen
    custom_button.place_forget()
    default_button.place_forget()

    start_timer()

def clicked_reset_button():
    # Stop timer
    window.after_cancel(timer)

    # Remove unnecessary widgets from the screen
    canvas.place_forget()
    button.place_forget()

    # Reset screen to the starting screen
    timer_label.config(text="Stretch Timer")
    default_button.place(relx=0.4,rely=0.6, anchor='center')
    custom_button.place(relx=0.6,rely=0.6, anchor='center')

    # Reset timer
    global reps
    reps = 0    

def clicked_snooze():
    # Stop the alarm
    pygame.mixer.music.stop()

    # Remove unnecessary widget from the screen
    button.place_forget()

    # Add work button to the screen
    work_button.config(command=clicked_work_from_snooze)
    work_button.place(relx=0.5, rely=0.7, anchor='center')

    # Decrease the reps so when the snooze timer finishes, the timer goes back to the stretch screen
    global reps
    reps -= 1

    # Start snooze timer
    snooze_sec = snooze_min * 60
    count_down(snooze_sec)

def clicked_work_from_snooze():
    # Increase the reps so the timer knows the user is ready to go back to work
    global reps
    reps += 1
    clicked_work()

def clicked_work():
    # Stop the alarm
    pygame.mixer.music.stop()

    # Remove unnecessary widget
    work_button.place_forget()

    # Stop snooze timer
    window.after_cancel(timer)

    start_timer()
# ---------------------------- SAVE USER INPUT ------------------------------- # 
def save_time_work():
    try:
        # Retrive the desired work time
        input = int(entry.get())

    # If the user did not enter an integer, display an error pop up    
    except ValueError:
        messagebox.showinfo(title="Error", message="Invalid input time. Try Again.")    
    else: 
        # Save the desired work time   
        global work_min
        work_min = input

        # Ask user for input and reconfigure to save the snooze time
        button.config(command=save_time_snooze)
        entry.bind('<Return>', (lambda event: save_time_snooze()))
        question_label.config(text="How long would you like to snooze?\n Enter in minutes")
        entry.delete(0, END)
        entry.insert(0, "5")

def save_time_snooze():
    try:
        # Retrive the desired snooze time
        input = int(entry.get())

    # If the user did not enter an integer, display an error pop up    
    except ValueError:
        messagebox.showinfo(title="Error", message="Invalid input time. Try Again.")    
    else:            
        global snooze_min
        snooze_min = input

        start_timer()

# ---------------------------- PLAY ALARM ------------------------------- # 
def play():
    pygame.mixer.music.load("alarm.wav")
    pygame.mixer.music.play(loops=1)

# ---------------------------- UI ------------------------------- # 
#Initialize and configure window
window = Tk()
window.title("Stretch Timer")
window.config(bg=DARK_COLOR)
window.geometry('600x500')

#Initialize and place on screen widgets
timer_label = Label(text="Stretch Timer", font=(FONT_NAME, 50, "bold"), fg=LIGHT_COLOR, bg=DARK_COLOR)
timer_label.place(relx=0.5,rely=0.25, anchor='center')
default_button = Button(text="Default", command=clicked_default_button, bg=LIGHT_COLOR, fg=DARK_COLOR,
                         font=(FONT_NAME, 15,"bold"), height=1, width=8)
default_button.place(relx=0.3,rely=0.6, anchor='center')
custom_button = Button(text="Custom", command=clicked_custom_button, bg=LIGHT_COLOR, fg=DARK_COLOR, 
                       font=(FONT_NAME, 15, "bold"), height=1, width=8)
custom_button.place(relx=0.7,rely=0.6, anchor='center')

#Initialize global widgets for later use
question_label = Label(font=(FONT_NAME, 18, "bold"), fg=LIGHT_COLOR, bg=DARK_COLOR)
entry = Entry(window, width=10, font=(FONT_NAME, 15,"bold"), justify= CENTER)
button = Button(text="Save", command=save_time_work, bg=LIGHT_COLOR, fg=DARK_COLOR, 
                font=(FONT_NAME, 15, "bold"), height=1, width=8)
canvas = Canvas(width=200, height=100, bg=DARK_COLOR, highlightthickness=0)
timer_text = canvas.create_text(100, 50, text="00:00", fill = LIGHT_COLOR, font=(FONT_NAME, 40, "bold"))
work_button = Button(text="Work", command=clicked_work, bg=LIGHT_COLOR, fg=DARK_COLOR, 
                     font=(FONT_NAME, 15, "bold"), height=1, width=8)
pygame.mixer.init()

#Initializing windows notification 
# Icon by Leremy https://www.freepik.com/icon/healthy_10049659#fromView=search&term=stretching&page=1&position=4&track=ais
toast = Notification(app_id="Stretch Timer", title="Get up and stretch!",
                     duration = "short", icon="C:/Users/Bailey/Documents/GitHub/Timer-App/notification_icon.png")
window.mainloop()