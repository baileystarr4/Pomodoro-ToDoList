from tkinter import *
from tkinter import messagebox
from notifier import *
import math
from to_do_list import *
from PIL import ImageTk,Image

class Timer:
    def __init__(self):
        self.DARK_COLOR = "#272829"
        self.LIGHT_COLOR = "#85a89b"
        self.FONT_NAME = "Courier"

        self.timer = None
        self.reps = 1
        self.total_pomos = 5
        self.work_min = 45
        self.short_break_min = 15
        self.long_break_min = 30
        self.paused = False

        # Initialize and configure window.
        self.window = Tk()
        self.window.title("Pomodoro")
        self.window.config(bg=self.DARK_COLOR)
        self.window.geometry('900x500')

        # Initialize and place on screen widgets.
        self.timer_label = Label(
            text="Pomodoro", 
            font=(self.FONT_NAME, 50, "bold"), 
            fg=self.LIGHT_COLOR, 
            bg=self.DARK_COLOR
        )
        self.timer_label.place(relx=0.5,rely=0.25, anchor='center')
        self.default_button = Button(
            text="Default", 
            command=self.clicked_default_button, 
            bg=self.LIGHT_COLOR, 
            activebackground= self.LIGHT_COLOR, 
            fg=self.DARK_COLOR, 
            font=(self.FONT_NAME, 15,"bold"), 
            height=1, 
            width=8
        )
        self.default_button.place(relx=0.3,rely=0.6, anchor='center')
        self.custom_button = Button(
            text="Custom", 
            command=self.clicked_custom_button, 
            bg=self.LIGHT_COLOR, 
            activebackground= self.LIGHT_COLOR, 
            fg=self.DARK_COLOR, 
            font=(self.FONT_NAME, 15, "bold"), 
            height=1, 
            width=8
        )
        self.custom_button.place(relx=0.7,rely=0.6, anchor='center')

        #Initialize icons for timer buttons.
        self.reset_icon = ImageTk.PhotoImage(Image.open("icons/reset_icon.png"))
        self.skip_icon = ImageTk.PhotoImage(Image.open("icons/skip_icon.png"))
        self.play_icon = ImageTk.PhotoImage(Image.open("icons/play_icon.png"))
        self.pause_icon = ImageTk.PhotoImage(Image.open("icons/pause_icon.png"))

        #Initialize widgets for later use.
        self.question_label = Label(
            font=(self.FONT_NAME, 18, "bold"), 
            fg=self.LIGHT_COLOR, 
            bg=self.DARK_COLOR
        )
        self.entry = Entry(
            self.window, 
            width=10, 
            font=(self.FONT_NAME, 15,"bold"), 
            justify= CENTER
        )
        self.save_button = Button(
            text="Save", 
            command=self.save_time_work, 
            bg=self.LIGHT_COLOR, 
            activebackground= self.LIGHT_COLOR, 
            fg=self.DARK_COLOR, 
            font=(self.FONT_NAME, 15, "bold"), 
            height=1, 
            width=8
        )
        self.pomos_label = Label(
            font=(self.FONT_NAME, 18, "bold"), 
            fg=self.LIGHT_COLOR, 
            bg=self.DARK_COLOR
        )
        self.timer_canvas = Canvas(
            width=200, 
            height=100, 
            bg=self.DARK_COLOR, 
            highlightthickness=0
        )
        self.timer_text = self.timer_canvas.create_text(
            100, 
            50, 
            text="00:00", 
            fill = self.LIGHT_COLOR,
            font=(self.FONT_NAME, 40, "bold")
        )
        self.skip_button = Button(
            image=self.skip_icon, 
            command=self.clicked_skip, 
            bg=self.DARK_COLOR, 
            activebackground= self.DARK_COLOR,
            border=0
        )
        self.pause_play_button = Button(
            image=self.pause_icon, 
            command=self.clicked_pause, 
            bg=self.DARK_COLOR, 
            activebackground= self.DARK_COLOR,
            border=0
        )
        self.reset_button = Button(
            image=self.reset_icon, 
            command=self.clicked_reset_button, 
            bg=self.DARK_COLOR, 
            activebackground= self.DARK_COLOR, 
            border=0
        )
        self.add_pomo_button = Button(
            text="Add Pomo", 
            command=self.clicked_add_pomo, 
            bg=self.LIGHT_COLOR,
            activebackground= self.LIGHT_COLOR, 
            fg=self.DARK_COLOR, 
            font=(self.FONT_NAME, 15, "bold"), 
            height=1, 
            width=8
        )
        self.finish_session_button = Button(
            text="Finish", 
            command=self.clicked_finish_button, 
            bg=self.LIGHT_COLOR, 
            activebackground= self.LIGHT_COLOR, 
            fg=self.DARK_COLOR, 
            font=(self.FONT_NAME, 15, "bold"), 
            height=1, 
            width=8
        )

        # Initilize to do list and notifier.
        self.to_do = ToDoList(self.window)
        self.notifier = Notifier()

        self.window.mainloop()

        # After the window closes, update the to do csv.
        self.to_do.update_csv()

    # ---------------------- BUTTON COMMANDS ---------------------- # 
    def clicked_default_button(self):
        self.custom_button.place_forget()
        self.default_button.place_forget()
        self.total_pomos = 5
        self.work_min = 45
        self.short_break_min = 15
        self.long_break_min = 30
        self.first_work_session()

    def clicked_custom_button(self):
        self.custom_button.place_forget()
        self.default_button.place_forget()

        # Ask for user input.
        self.question_label.config(
            text="How long would you like to work? \n Enter in minutes"
        )
        self.question_label.place(relx=0.5,rely=0.425, anchor='center')

        # Add entry and save button widgets to the screen.
        self.entry.place(relx=0.5,rely=0.55, anchor='center')
        self.entry.focus()
        self.entry.delete(0, END)
        self.entry.insert(0, "30")
        self.entry.bind('<Return>', (lambda event: self.save_time_work()))
        self.save_button.config(command=self.save_time_work)
        self.save_button.place(relx=0.5,rely=0.7, anchor='center')

    def clicked_reset_button(self, reset_alert = True):
        if reset_alert:
            self.clicked_pause()
            result = mb.askquestion(
                'Reset Pomodoro Timer', 'Are you sure you want to reset?'
            )
            if result == 'no':
                self.clicked_play()
                return
            
        # Stop timer.
        self.window.after_cancel(self.timer)

        # Remove unnecessary widgets from the screen.
        self.timer_canvas.place_forget()
        self.reset_button.place_forget()
        self.pause_play_button.place_forget()
        self.skip_button.place_forget()
        self.pomos_label.place_forget()

        # Reset reps and pause / play button
        self.reps = 1
        self.pause_play_button.config(
            image=self.pause_icon, 
            command=self.clicked_pause
        )
        self.paused = False

        # Reset to the starting screen.
        self.timer_label.config(text="Pomodoro")
        self.default_button.place(relx=0.3,rely=0.6, anchor='center')
        self.save_button.config(command=self.save_time_work)
        self.custom_button.place(relx=0.7,rely=0.6, anchor='center')  

    def clicked_pause(self):
        self.paused = True
        self.pause_play_button.config(
            command=self.clicked_play, 
            image=self.play_icon
        )
    
    def clicked_play(self):
        self.paused = False
        self.pause_play_button.config(
            command=self.clicked_pause, 
            image=self.pause_icon
        )

    def clicked_skip(self):
        # Set pause to false so the next session can start properly.
        self.paused = False
        # Stop and restart timer with no alarm.
        self.window.after_cancel(self.timer)
        self.start_timer(alarm=False)

    def start_next_session(self, session):
        # Stop alarm, reconfigure the pause/play button to pause, 
        # and start the count down.
        self.notifier.stop_sound()
        self.pause_play_button.config(
            command=self.clicked_pause, 
            image=self.pause_icon
        )

        if session == "work":
            seconds = self.work_min * 60
        elif session == "long":
            seconds = self.long_break_min * 60
        elif session == "short":
            seconds = self.short_break_min * 60

        self.count_down(seconds) 

    def clicked_add_pomo(self):
        self.add_pomo_button.place_forget()
        self.finish_session_button.place_forget()

        # Ask for user input.
        self.question_label.config(text="How many more would you like to add?")

        # Add entry and save button widgets to the screen.
        self.entry.place(relx=0.5,rely=0.55, anchor='center')
        self.entry.focus()
        self.entry.delete(0, END)
        self.entry.insert(0, "1")
        self.entry.bind(
            '<Return>', 
            (lambda event: self.save_total_pomos(adding = True))
        )
        self.save_button.config(command=lambda: self.save_total_pomos(adding=True))
        self.save_button.place(relx=0.5,rely=0.7, anchor='center')

    def clicked_finish_button(self):
        self.question_label.place_forget()
        self.add_pomo_button.place_forget()
        self.finish_session_button.place_forget()
        self.clicked_reset_button(reset_alert=False)

    # ---------------------- SAVE USER INPUT ---------------------- # 
    def try_to_get_input(self):
        try:
            input = int(self.entry.get())

        # If the user did not enter an integer, 
        # display an error pop up and return 0 to try again. 
        except ValueError:
            messagebox.showinfo(title="Error", message="Invalid input time. Try Again.")
            return 0
        else:
            return input
        
    def save_time_work(self):  
        self.work_min = self.try_to_get_input()

        if self.work_min != 0:
            # Ask user for short break time and reconfigure the save button
            self.save_button.config(command=self.save_time_short_break)
            self.entry.bind(
                '<Return>', 
                (lambda event: self.save_time_short_break())
            )
            self.question_label.config(
                text="How long would you like the short break to be?\n Enter in minutes"
            )
            self.entry.delete(0, END)
            self.entry.insert(0, "5")

    def save_time_short_break(self):
        self.short_break_min = self.try_to_get_input()

        if self.short_break_min != 0:
            # Ask user for long break time and reconfigure the save button
            self.save_button.config(command=self.save_time_long_break)
            self.entry.bind(
                '<Return>', 
                (lambda event: self.save_time_long_break())
            )
            self.question_label.config(
                text="How long would you like the long break to be?\n Enter in minutes"
            )
            self.entry.delete(0, END)
            self.entry.insert(0, "15")

    def save_time_long_break(self):
        self.long_break_min = self.try_to_get_input()

        if self.long_break_min != 0:
            # Ask user for total pomos and reconfigure the save button
            self.save_button.config(command=self.save_total_pomos)
            self.entry.bind(
                '<Return>', 
                (lambda event: self.save_total_pomos())
            )
            self.question_label.config(
                text="How many pomodoros would you like to do?"
            )
            self.entry.delete(0, END)
            self.entry.insert(0, "5")
    
    def save_total_pomos(self, adding = False):
        if adding == True:
            self.total_pomos = self.try_to_get_input() + self.total_pomos
        else:
            self.total_pomos = self.try_to_get_input()

        if self.total_pomos != 0:
            # Remove unnecessary widgets from the screen
            self.entry.unbind('<Return>')
            self.question_label.place_forget()
            self.entry.place_forget()       
            self.save_button.place_forget()

            self.first_work_session()        

    # ---------------------------- TIMER ------------------------------- # 
    def start_timer(self, alarm = True):
        self.reps += 1

        # Have you completed all the scheduled pomodoros?
        # Would you like to add another or finish?
        if ((self.reps//2)) == self.total_pomos:
            # Remove unnecessary widgets from the screen
            self.timer_canvas.place_forget()
            self.reset_button.place_forget()
            self.pause_play_button.place_forget()
            self.skip_button.place_forget()

            # Show end screen
            self.timer_label.config(
                text=f"{self.total_pomos} Pomodoros Completed!"
            )
            self.question_label.config(
                text="Would you like to add another pomodoro?"
            )
            self.question_label.place(relx=0.5,rely=0.425, anchor='center')
            self.add_pomo_button.place(relx=0.3,rely=0.6, anchor='center')
            self.finish_session_button.place(relx=0.7,rely=0.6, anchor='center')
            
            self.notifier.notify("end")

        # Is it time for a long break?
        elif self.reps % 6 == 0:
            self.timer_canvas.itemconfig(
                self.timer_text, 
                text=f"{self.long_break_min}:00"
            )
            self.timer_label.config(text="Long Break")
            self.pause_play_button.config(
                command=(lambda: self.start_next_session("long")),
                image=self.play_icon
            )
            if alarm:
                self.notifier.notify("long break")

        # Is it time for a short break?
        elif self.reps % 2 == 0:
            self.timer_canvas.itemconfig(
                self.timer_text, 
                text=f"{self.short_break_min}:00"
            )
            self.timer_label.config(text="Short Break")
            self.pause_play_button.config(
                command=(lambda: self.start_next_session("short")),
                image=self.play_icon
            )
            if alarm:
                self.notifier.notify("short break")

        # If not, it's time to work.
        else:
            self.timer_label.config(text="Work")
            self.pomos_label.config(
                text=f"{(self.reps//2)+1}/{self.total_pomos}"
            )
            self.timer_canvas.itemconfig(
                self.timer_text, 
                text=f"{self.work_min}:00"
            )
            self.pause_play_button.config(
                command=(lambda: self.start_next_session("work")),
                image=self.play_icon
            )
            if alarm:
                self.notifier.notify("work")    

    def count_down(self,count):
        count_min = math.floor(count / 60)
        count_sec = count % 60

        if count_min < 10:
            count_min=f"0{count_min}"
        if count_sec < 10:
            count_sec=f"0{count_sec}"

        # Update timer on screen.
        self.timer_canvas.itemconfig(
            self.timer_text, 
            text=f"{count_min}:{count_sec}"
        )

        # If the timer has not ended and is not paused, 
        # continue counting down.
        if count:
            if not self.paused:
                count -= 1
            self.timer = self.window.after(1000, self.count_down, count) 
        else:
            self.start_timer()

# ---------------------------- HELPERS  ---------------------------- # 
    def place_timer_buttons(self):
        self.reset_button.place(relx=0.3,rely=0.7, anchor='center')
        self.pause_play_button.place(relx=0.5,rely=0.7, anchor='center')
        self.skip_button.place(relx=0.7,rely=0.7, anchor='center')

    def first_work_session(self):
        self.place_timer_buttons()

        #Configure and place timer screen.
        self.pomos_label.config(text=f"{(self.reps//2)+1}/{self.total_pomos}")
        self.pomos_label.place(relx=0.5,rely=0.1, anchor='center')
        self.timer_label.config(text="Work")
        self.timer_canvas.place(relx=0.5,rely=0.475, anchor='center')

        self.start_next_session("work")
