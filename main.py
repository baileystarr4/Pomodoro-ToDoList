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
    timer_label.config(text="Timer")
    # canvas.itemconfig(timer_text, text="00:00")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1

    # work_sec = work_min * 60
    # short_sec = SHORT_BREAK_MIN * 60
    # long_sec = LONG_BREAK_MIN * 60
    
    # if reps % 8 == 0:
    #     count_down(long_sec)
    #     timer_label.config(text="Break", fg=DEFAULT_TEXT)
    # elif reps % 2 == 0:
    #     count_down(short_sec)
    #     timer_label.config(text="Break", fg=DEFAULT_TEXT)
    # else:
    #     count_down(work_sec)
    #     timer_label.config(text="Work", fg=DEFAULT_TEXT)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_min < 10:
        count_min=f"0{count_min}"
    if count_sec < 10:
        count_sec=f"0{count_sec}"

    # canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()

# ----------------------------------------------------------- # 
def save_time_work():
    input = work_time_entry.get()
    global work_min
    work_min = input
    timer_label.config(text=work_min)
    
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Timer")
window.config(padx=150, pady=100, bg=DEFAULT_BG)

timer_label = Label(text="Timer", font=(FONT_NAME, 50, "bold"), fg=DEFAULT_TEXT, bg=DEFAULT_BG)
timer_label.grid(column=1, row=0)

work_time_entry = Entry(window, width=10)
work_time_entry.grid(column=1, row=1)


button = Button(text="save", command=save_time_work)
button.grid(column=1, row=2)
# start_button = Button(text="Start", command=start_timer)
# start_button.grid(column=0, row=2)

# reset_button = Button(text="Reset", command=clicked_reset_button)
# reset_button.grid(column=2, row=2)

# canvas = Canvas(width=200, height=224, bg=DEFAULT_BG, highlightthickness=0)
# timer_text = canvas.create_text(100, 130, text="00:00", fill = "white", font=(FONT_NAME, 35, "bold"))
# canvas.grid(column=1, row=1)

window.mainloop()