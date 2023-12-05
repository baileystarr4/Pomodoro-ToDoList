from tkinter import *
from tkinter import messagebox
from Notifier import *
import math

class UI:
    def __init__(self):
        self.DARK_COLOR = "#272829"
        self.LIGHT_COLOR = "#D8D9DA"
        self.FONT_NAME = "Courier"

        self.timer = None
        self.notifier = Notifier()
        self.reps = 0
        self.work_min = 45
        self.short_break = 15
        self.long_break = 30

        #Initialize and configure window
        self.window = Tk()
        self.window.title("Pomodoro")
        self.window.config(bg=self.DARK_COLOR)
        self.window.geometry('600x500')

        #Initialize and place on screen widgets
        self.timer_label = Label(text="Pomodoro", font=(self.FONT_NAME, 50, "bold"), fg=self.LIGHT_COLOR, bg=self.DARK_COLOR)
        self.timer_label.place(relx=0.5,rely=0.25, anchor='center')
        self.default_button = Button(text="Default", command=self.clicked_default_button, bg=self.LIGHT_COLOR, fg=self.DARK_COLOR,
                                font=(self.FONT_NAME, 15,"bold"), height=1, width=8)
        self.default_button.place(relx=0.3,rely=0.6, anchor='center')
        self.custom_button = Button(text="Custom", command=self.clicked_custom_button, bg=self.LIGHT_COLOR, fg=self.DARK_COLOR, 
                            font=(self.FONT_NAME, 15, "bold"), height=1, width=8)
        self.custom_button.place(relx=0.7,rely=0.6, anchor='center')

        #Initialize widgets for later use
        self.question_label = Label(font=(self.FONT_NAME, 18, "bold"), fg=self.LIGHT_COLOR, bg=self.DARK_COLOR)
        self.entry = Entry(self.window, width=10, font=(self.FONT_NAME, 15,"bold"), justify= CENTER)
        self.canvas = Canvas(width=200, height=100, bg=self.DARK_COLOR, highlightthickness=0)
        self.timer_text = self.canvas.create_text(100, 50, text="00:00", fill = self.LIGHT_COLOR, font=(self.FONT_NAME, 40, "bold"))
        self.save_button = Button(text="Save", command=self.save_time_work, bg=self.LIGHT_COLOR, fg=self.DARK_COLOR, 
                        font=(self.FONT_NAME, 15, "bold"), height=1, width=8)
        self.reset_button = Button(text="Reset", command=self.clicked_reset_button, bg=self.LIGHT_COLOR, fg=self.DARK_COLOR, 
                        font=(self.FONT_NAME, 15, "bold"), height=1, width=8)
        self.work_button = Button(text="Work", command=self.clicked_work, bg=self.LIGHT_COLOR, fg=self.DARK_COLOR, 
                            font=(self.FONT_NAME, 15, "bold"), height=1, width=8) 
        self.break_button = Button(text="Break", command=self.clicked_break, bg=self.LIGHT_COLOR, fg=self.DARK_COLOR, 
                            font=(self.FONT_NAME, 15, "bold"), height=1, width=8)
        self.window.mainloop()

    # ---------------------------- BUTTON COMMANDS ------------------------------- # 
    def clicked_custom_button(self):
        # Remove unnecessary widgets from the screen
        self.custom_button.place_forget()
        self.default_button.place_forget()

        # Ask for user input
        self.question_label.config(text="How long would you like to work? \n Enter in minutes")
        self.question_label.place(relx=0.5,rely=0.425, anchor='center')

        # Add entry and save button widgets to the screen
        self.entry.place(relx=0.5,rely=0.55, anchor='center')
        self.entry.focus()
        self.entry.delete(0, END)
        self.entry.insert(0, "30")
        self.entry.bind('<Return>', (lambda event: self.save_time_work()))
        self.save_button.place(relx=0.5,rely=0.7, anchor='center')

    def clicked_default_button(self):
        # Remove unnecessary widgets from the screen
        self.custom_button.place_forget()
        self.default_button.place_forget()

        self.start_timer()

    def clicked_reset_button(self):
        # Stop timer
        self.window.after_cancel(self.timer)
        # Stop the alarm
        self.notifier.stop_music()

        # Remove unnecessary widgets from the screen
        self.canvas.place_forget()
        self.reset_button.place_forget()

        # Reset screen to the starting screen
        self.timer_label.config(text="Stretch Timer")
        self.default_button.place(relx=0.3,rely=0.6, anchor='center')
        self.custom_button.place(relx=0.7,rely=0.6, anchor='center')

        # Reset timer
        self.reps = 0    

    def clicked_snooze(self):
        # Stop the alarm
        self.notifier.stop_music()

        # Remove unnecessary widget from the screen
        self.button.place_forget()

        # Add work button to the screen
        self.work_button.config(command=self.clicked_work_from_snooze)
        self.work_button.place(relx=0.5, rely=0.7, anchor='center')

        # Decrease the reps so when the snooze timer finishes, the timer goes back to the stretch screen
        self.reps -= 1

        # Start snooze timer
        snooze_sec = self.snooze_min * 60
        self.count_down(snooze_sec)

    def clicked_work_from_snooze(self):
        # Increase the reps so the timer knows the user is ready to go back to work
        self.reps += 1
        self.clicked_work()

    def clicked_work(self):
        # Stop the alarm
        self.notifier.stop_music()

        # Remove unnecessary widget
        self.work_button.place_forget()

        # Stop snooze timer
        self.window.after_cancel(self.timer)

        self.start_timer()
    # ---------------------------- SAVE USER INPUT ------------------------------- # 
    def save_time_work(self):
        try:
            # Retrive the desired work time
            input = int(self.entry.get())

        # If the user did not enter an integer, display an error pop up    
        except ValueError:
            messagebox.showinfo(title="Error", message="Invalid input time. Try Again.")    
        else: 
            # Save the desired work time   
            self.work_min = input

            # Ask user for input and reconfigure to save the snooze time
            self.save_button.config(command=self.save_time_snooze)
            self.entry.bind('<Return>', (lambda event: self.save_time_snooze()))
            self.question_label.config(text="How long would you like to break?\n Enter in minutes")
            self.entry.delete(0, END)
            self.entry.insert(0, "5")

    def save_time_snooze(self):
        try:
            # Retrive the desired snooze time
            input = int(self.entry.get())

        # If the user did not enter an integer, display an error pop up    
        except ValueError:
            messagebox.showinfo(title="Error", message="Invalid input time. Try Again.")    
        else:            
            self.short_break = input
            self.save_button.place_forget()
            self.start_timer()

    # ---------------------------- UPDATING THE SCREEN ------------------------------- # 
    def config_for_work(self):
        # Remove unnecessary widgets from the screen
        self.entry.unbind('<Return>')
        self.question_label.place_forget()
        self.entry.place_forget()

        self.timer_label.config(text="Work")
        self.reset_button.place(relx=0.5,rely=0.7, anchor='center')

    def config_for_stretch(self):
        self.timer_label.config(text="STRETCH")
        self.canvas.place_forget()
        self.work_button.config(command=self.clicked_work)
        self.work_button.place(relx=0.3, rely=0.6, anchor='center')
        self.break_button.place(relx=0.7, rely=0.6, anchor='center')

    # ---------------------------- TIMER ------------------------------- # 
    def start_timer(self):
        self.reps += 1
        
        # Is it time to stretch?
        if self.reps % 2 == 0:
            self.config_for_stretch()
            self.notifier.break_toast.show()
            self.notifier.play_alarm()

        # If not, it's time to work
        else:
            self.config_for_work()
            self.notifier.work_toast.show()
            self.notifier.play_alarm()
            work_sec = self.work_min * 60
            self.count_down(work_sec)    

    def count_down(self,count):
        # Count down mechanism
        count_min = math.floor(count / 60)
        count_sec = count % 60
        if count_min < 10:
            count_min=f"0{count_min}"
        if count_sec < 10:
            count_sec=f"0{count_sec}"

        # Update timer on screen
        self.canvas.place(relx=0.5,rely=0.475, anchor='center')
        self.canvas.itemconfig(self.timer_text, text=f"{count_min}:{count_sec}")

        # If the timer has not ended, continue counting down
        if count > 0:
            self.timer = self.window.after(1000, self.count_down, count - 1)
        # Otherwise, stop counting and start the timer again    
        else:
            self.start_timer()