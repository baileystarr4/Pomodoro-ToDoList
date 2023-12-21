from tkinter import *
from tkinter import messagebox
from Notifier import *
import math
from ToDoList import *
from PIL import ImageTk,Image

class UI:
    def __init__(self):
        self.DARK_COLOR = "#272829"
        self.LIGHT_COLOR = "#85a89b"
        self.FONT_NAME = "Courier"

        self.timer = None
        self.notifier = Notifier()
        self.reps = 0
        self.total_pomos = 5
        self.work_min = 45
        self.short_break_min = 15
        self.long_break_min = 30
        self.paused = False

        # Initialize and configure window
        self.window = Tk()
        self.window.title("Pomodoro")
        self.window.config(bg=self.DARK_COLOR)
        self.window.geometry('900x500')

        # Initialize and place on screen widgets
        self.timer_label = Label(text="Pomodoro", font=(self.FONT_NAME, 50, "bold"), fg=self.LIGHT_COLOR, bg=self.DARK_COLOR)
        self.timer_label.place(relx=0.5,rely=0.25, anchor='center')
        self.default_button = Button(text="Default", command=self.clicked_default_button, bg=self.LIGHT_COLOR, activebackground= self.LIGHT_COLOR, fg=self.DARK_COLOR,
                                font=(self.FONT_NAME, 15,"bold"), height=1, width=8)
        self.default_button.place(relx=0.3,rely=0.6, anchor='center')
        self.custom_button = Button(text="Custom", command=self.clicked_custom_button, bg=self.LIGHT_COLOR, activebackground= self.LIGHT_COLOR, fg=self.DARK_COLOR, 
                            font=(self.FONT_NAME, 15, "bold"), height=1, width=8)
        self.custom_button.place(relx=0.7,rely=0.6, anchor='center')

        # Initilize to do list
        self.to_do = ToDoList(self.window)
 
        # Initilize to do list
        self.to_do = ToDoList(self.window)

        #Initialize widgets for later use
        self.question_label = Label(font=(self.FONT_NAME, 18, "bold"), fg=self.LIGHT_COLOR, bg=self.DARK_COLOR)
        self.entry = Entry(self.window, width=10, font=(self.FONT_NAME, 15,"bold"), justify= CENTER)
        self.canvas = Canvas(width=200, height=100, bg=self.DARK_COLOR, highlightthickness=0)
        self.timer_text = self.canvas.create_text(100, 50, text="00:00", fill = self.LIGHT_COLOR, font=(self.FONT_NAME, 40, "bold"))
        self.save_button = Button(text="Save", command=self.save_time_work, bg=self.LIGHT_COLOR, activebackground= self.LIGHT_COLOR, fg=self.DARK_COLOR, 
                        font=(self.FONT_NAME, 15, "bold"), height=1, width=8)
        self.work_button = Button(text="Work", command=self.clicked_work, bg=self.LIGHT_COLOR, fg=self.DARK_COLOR, 
                            font=(self.FONT_NAME, 15, "bold"), height=1, width=8) 
        self.break_button = Button(text="Break", command=self.clicked_short_break, bg=self.LIGHT_COLOR, fg=self.DARK_COLOR, 
                            font=(self.FONT_NAME, 15, "bold"), height=1, width=8)
        self.pomos_label = Label(font=(self.FONT_NAME, 18, "bold"), fg=self.LIGHT_COLOR, bg=self.DARK_COLOR)
        self.add_pomo_button = Button(text="Add Pomo", command=self.clicked_add_pomo, bg=self.LIGHT_COLOR, activebackground= self.LIGHT_COLOR, fg=self.DARK_COLOR, 
                            font=(self.FONT_NAME, 15, "bold"), height=1, width=8)
        self.finish_session_button = Button(text="Finish", command=self.clicked_finish_button, bg=self.LIGHT_COLOR, activebackground= self.LIGHT_COLOR, fg=self.DARK_COLOR, 
                            font=(self.FONT_NAME, 15, "bold"), height=1, width=8)
        self.reset_icon = ImageTk.PhotoImage(Image.open("icons/reset_icon.png"))
        self.skip_icon = ImageTk.PhotoImage(Image.open("icons/skip_icon.png"))
        self.play_icon = ImageTk.PhotoImage(Image.open("icons/play_icon.png"))
        self.pause_icon = ImageTk.PhotoImage(Image.open("icons/pause_icon.png"))
        self.skip_button = Button(image=self.skip_icon, command=self.clicked_skip, bg=self.DARK_COLOR, activebackground= self.DARK_COLOR, border=0)
        self.pause_play_button = Button(image=self.pause_icon, command=self.clicked_pause, bg=self.DARK_COLOR, activebackground= self.DARK_COLOR, border=0)
        self.reset_button = Button(image=self.reset_icon, command=self.clicked_reset_button, bg=self.DARK_COLOR, activebackground= self.DARK_COLOR, border=0)
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

        self.reset_button.place(relx=0.3,rely=0.7, anchor='center')
        self.pause_play_button.place(relx=0.5,rely=0.7, anchor='center')
        self.skip_button.place(relx=0.7,rely=0.7, anchor='center')

        self.start_timer()

    def clicked_reset_button(self, refresh_msg = True):
        if refresh_msg:
            self.clicked_pause()
            result = mb.askquestion('Reset Pomodoro Timer', 'Are you sure you want to reset?')
            if result == 'no':
                self.clicked_play()
                return
        # Stop timer
        self.window.after_cancel(self.timer)
        # Stop the alarm
        self.notifier.stop_music()
        self.window.unbind('<space>')

        # Remove unnecessary widgets from the screen
        self.canvas.place_forget()
        self.reset_button.place_forget()
        self.pause_play_button.place_forget()
        self.skip_button.place_forget()
        self.pomos_label.place_forget()

        # Reset default settings
        self.total_pomos = 5
        self.total_pomos = 5
        self.work_min = 45
        self.short_break_min = 15
        self.long_break_min = 30

        # Reset screen to the starting screen
        self.timer_label.config(text="Pomodoro")
        self.default_button.place(relx=0.3,rely=0.6, anchor='center')
        self.save_button.config(command=self.save_time_work)
        self.custom_button.place(relx=0.7,rely=0.6, anchor='center')

        # Reset timer
        self.reps = 0    

    def clicked_work(self):
        # Stop alarm, update screen, and start the count down
        self.notifier.stop_music()
        
        self.pause_play_button.config(command=self.clicked_pause, image=self.pause_icon)

        work_sec = self.work_min * 60
        self.count_down(work_sec) 

    def clicked_long_break(self):
        # Stop alarm, update screen, and start the count down
        self.notifier.stop_music()

        self.pause_play_button.config(command=self.clicked_pause, image=self.pause_icon)

        break_sec = self.long_break_min * 60
        self.count_down(break_sec)

    def clicked_short_break(self):
        # Stop alarm, update screen, and start the count down
        self.notifier.stop_music()

        self.pause_play_button.config(command=self.clicked_pause, image=self.pause_icon)

        break_sec = self.short_break_min * 60
        self.count_down(break_sec)

    def clicked_pause(self):
        self.paused = True
        self.pause_play_button.config(command=self.clicked_play, image=self.play_icon)
        self.window.bind('<space>', (lambda event: self.clicked_play()))
    
    def clicked_play(self):
        self.paused = False
        self.pause_play_button.config(command=self.clicked_pause, image=self.pause_icon)
        self.window.bind('<space>', (lambda event: self.clicked_pause()))

    def clicked_skip(self):
        self.paused = False
        self.window.after_cancel(self.timer)
        self.start_timer()

    def clicked_add_pomo(self):
        self.question_label.place_forget()
        self.add_pomo_button.place_forget()
        self.finish_session_button.place_forget()
        self.total_pomos += 1
        self.reps += 1
        self.canvas.place(relx=0.5,rely=0.475, anchor='center')
        self.clicked_work()

    def clicked_finish_button(self):
        self.question_label.place_forget()
        self.add_pomo_button.place_forget()
        self.finish_session_button.place_forget()
        self.clicked_reset_button(refresh_msg=False)

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

            # Ask user for input and reconfigure to save the short break time
            self.save_button.config(command=self.save_time_short_break)
            self.entry.bind('<Return>', (lambda event: self.save_time_short_break()))
            self.question_label.config(text="How long would you like the short break to be?\n Enter in minutes")
            self.entry.delete(0, END)
            self.entry.insert(0, "5")

    def save_time_short_break(self):
        try:
            # Retrive the desired short break time
            input = int(self.entry.get())

        # If the user did not enter an integer, display an error pop up    
        except ValueError:
            messagebox.showinfo(title="Error", message="Invalid input time. Try Again.")    
        else:            
            self.short_break_min = input

            # Ask user for input and reconfigure to save the long break time
            self.save_button.config(command=self.save_time_long_break)
            self.entry.bind('<Return>', (lambda event: self.save_time_long_break()))
            self.question_label.config(text="How long would you like the long break to be?\n Enter in minutes")
            self.entry.delete(0, END)
            self.entry.insert(0, "15")

    def save_time_long_break(self):
        try:
            # Retrive the desired long break time
            input = int(self.entry.get())

        # If the user did not enter an integer, display an error pop up    
        except ValueError:
            messagebox.showinfo(title="Error", message="Invalid input time. Try Again.")    
        else:            
            self.long_break_min = input    

            # Ask user for input and reconfigure to save the total pomos
            self.save_button.config(command=self.save_total_pomos)
            self.entry.bind('<Return>', (lambda event: self.save_total_pomos()))
            self.question_label.config(text="How many pomodoros would you like to do?")
            self.entry.delete(0, END)
            self.entry.insert(0, "5")
    
    def save_total_pomos(self):
        try:
            # Retrive the desired amount of pomos
            input = int(self.entry.get())

        # If the user did not enter an integer, display an error pop up    
        except ValueError:
            messagebox.showinfo(title="Error", message="Invalid input. Try Again.")    
        else:            
            self.total_pomos = input    

            # Remove unnecessary widgets from the screen
            self.entry.unbind('<Return>')
            self.question_label.place_forget()
            self.entry.place_forget()       
            self.save_button.place_forget()

            self.reset_button.place(relx=0.3,rely=0.7, anchor='center')
            self.pause_play_button.place(relx=0.5,rely=0.7, anchor='center')
            self.skip_button.place(relx=0.7,rely=0.7, anchor='center')

            self.start_timer()        

    # ---------------------------- TIMER ------------------------------- # 
    def start_timer(self):
        self.reps += 1

        # Have you completed all the scheduled pomodoros?
        # Would you like to add another or finish?
        if ((self.reps//2)) == self.total_pomos:
            self.canvas.place_forget()
            self.reset_button.place_forget()
            self.pause_play_button.place_forget()
            self.skip_button.place_forget()
            self.pomos_label.config(text=f"{self.total_pomos}/{self.total_pomos}")
            self.timer_label.config(text=f"{self.total_pomos} Pomodoros Completed!")
            self.question_label.config(text="Would you like to add another pomodoro?")

            self.question_label.place(relx=0.5,rely=0.425, anchor='center')
            self.add_pomo_button.place(relx=0.3,rely=0.6, anchor='center')
            self.finish_session_button.place(relx=0.7,rely=0.6, anchor='center')
            # ADD toast noti. for finished
            self.notifier.play_alarm()

        # Is it time for a long break?
        elif self.reps % 6 == 0:
            self.canvas.itemconfig(self.timer_text, text=f"{self.long_break_min}:00")
            self.timer_label.config(text="Long Break")
            self.pause_play_button.config(command=self.clicked_long_break, image=self.play_icon)
            self.notifier.long_break_toast.show()
            self.notifier.play_alarm()

        # Is it time for a short break?
        elif self.reps % 2 == 0:
            self.canvas.itemconfig(self.timer_text, text=f"{self.short_break_min}:00")
            self.timer_label.config(text="Short Break")
            self.pause_play_button.config(command=self.clicked_short_break, image=self.play_icon)
            self.notifier.short_break_toast.show()
            self.notifier.play_alarm()

        # If not, it's time to work
        else:
            self.timer_label.config(text="Work")
            # If it's not our first work session, show the work button to start
            if self.reps != 1: 
                self.pomos_label.config(text=f"{(self.reps//2)+1}/{self.total_pomos}")
                self.canvas.itemconfig(self.timer_text, text=f"{self.work_min}:00")
                self.pause_play_button.config(command=self.clicked_work, image=self.play_icon)
                self.notifier.work_toast.show()
                self.notifier.play_alarm()

            # If it is the first work session, start timer immediately 
            else: 
                self.pomos_label.config(text=f"1/{self.total_pomos}")
                self.pomos_label.place(relx=0.5,rely=0.1, anchor='center')
                self.canvas.place(relx=0.5,rely=0.475, anchor='center')
                work_sec = self.work_min * 60
                self.window.bind('<space>', (lambda event: self.clicked_pause()))
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
        self.canvas.itemconfig(self.timer_text, text=f"{count_min}:{count_sec}")

        # If the timer has not ended, continue counting down
        if count:
            if not self.paused:
                count -= 1
            self.timer = self.window.after(1000, self.count_down, count)
        # Otherwise, stop counting and start the timer again    
        else:
            self.start_timer()