from tkinter import *
import math
#TO DO 
# 1) Make reps, work minutes, snooze time customizable. 
# 2) Add use default button
# 3) Fix UI
# 4) Make into a Windows App
# 5) Windows Pop Ups?

# ---------------------------- CONSTANTS ------------------------------- #
DEFAULT_BG = "#272829"
DEFAULT_BUTTON = "#61677A"
DEFAULT_TEXT = "#D8D9DA"
FONT_NAME = "Courier"
work_min = 0
snooze_min = 0
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def clicked_reset_button():
    window.after_cancel(timer)
    canvas.grid_remove()
    timer_label.config(text="Timer")
    question_label.config(text="How long would you like to work? \n Enter in minutes")
    question_label.grid()
    entry.grid()
    button.config(text="save", command=save_time_work)
    
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    global work_min
    global snooze_min
    reps += 1

    work_sec = work_min * 60
    snooze_sec = snooze_min * 60

    question_label.grid_remove()
    button.config(text="reset", command=clicked_reset_button)
    entry.grid_remove()
    canvas.grid(column=1, row=1)
    
    if reps % 2 == 0:
        count_down(snooze_sec)
        timer_label.config(text="Break", fg=DEFAULT_TEXT)
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=DEFAULT_TEXT)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_min < 10:
        count_min=f"0{count_min}"
    if count_sec < 10:
        count_sec=f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()

# ----------------------------------------------------------- #
def clicked_custom_button():
    custom_button.grid_remove()
    default_button.grid_remove()
    question_label.config(text="How long would you like to work? \n Enter in minutes")
    question_label.grid(column=1, row=1)
    entry.grid(column=1, row=2)
    button.grid(column=1, row=3)

def clicked_default_button():
    custom_button.grid_remove()
    default_button.grid_remove()
    global work_min
    global snooze_min

    work_min = 60
    snooze_min = 10
    button.grid(column=1, row=3)
    start_timer()
def save_time_work():
    input = int(entry.get())
    global work_min
    work_min = input

    button.config(command=save_time_snooze)
    question_label.config(text="How long would you like to snooze?\n Enter in minutes")

def save_time_snooze():
    input = int(entry.get())
    global snooze_min
    snooze_min = input
    start_timer()

    
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Timer")
window.config(padx=150, pady=100, bg=DEFAULT_BG)

timer_label = Label(text="Stretching Timer", font=(FONT_NAME, 50, "bold"), fg=DEFAULT_TEXT, bg=DEFAULT_BG)
timer_label.grid(column=1, row=0)
default_button = Button(text="Default", command=clicked_default_button)
default_button.grid(column=0, row=1)
custom_button = Button(text="Custom", command=clicked_custom_button)
custom_button.grid(column=1, row=1)

question_label = Label(font=(FONT_NAME, 18), fg=DEFAULT_TEXT, bg=DEFAULT_BG)
entry = Entry(window, width=10)
button = Button(text="save", command=save_time_work)
canvas = Canvas(width=200, height=224, bg=DEFAULT_BG, highlightthickness=0)
timer_text = canvas.create_text(100, 130, text="00:00", fill = "white", font=(FONT_NAME, 35, "bold"))

window.mainloop()