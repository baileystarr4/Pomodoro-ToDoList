from tkinter import *
from tkinter import messagebox as mb
from PIL import ImageTk,Image
import pandas

class ToDoList:
    def __init__(self, window):
        self.active_tasks = {}
        self.completed_tasks = {}
        self.queued_tasks = {}
        self.ACTIVE_TASK_FONT = ("Courier", 12, "bold")
        self.FINISHED_TASK_FONT = ("Courier", 12, "overstrike")
        self.LIGHT_COLOR = "#5C8374"
        self.DARK_COLOR = "#272829"

        # Store root window and initilaze to do list frame
        self.window = window
        self.frame = Frame(self.window,width=300,height=500,bg=self.LIGHT_COLOR)
        self.window.bind('<t>', (lambda event: self.toggle_frame()))

        # Initialize and place the open to do list button onto the root window
        self.list_icon = ImageTk.PhotoImage(Image.open("icons/list_icon.png"))
        self.open_to_do = Button(self.window, image=self.list_icon, command=self.toggle_frame, 
                                 border=0, bg=self.DARK_COLOR, activebackground=self.DARK_COLOR)
        self.open_to_do.place(x=10,y=15)
        
        # Initialize the widgets used when the to do list frame is opened
        self.close_icon = ImageTk.PhotoImage(Image.open("icons/close_icon.png"))
        self.close_to_do = Button(self.frame, image=self.close_icon, border=0, 
                                  command=self.close_task_list, bg=self.LIGHT_COLOR, 
                                  activebackground=self.LIGHT_COLOR)
        self.add_icon = ImageTk.PhotoImage(Image.open("icons/add_icon.png"))
        self.add_task_button = Button(self.frame, image=self.add_icon, border=0,
                                      command=self.add_task, bg=self.LIGHT_COLOR, 
                                      activebackground=self.LIGHT_COLOR)
        self.refresh_icon = ImageTk.PhotoImage(Image.open("icons/refresh_icon.png"))
        self.refresh_button = Button(self.frame, image=self.refresh_icon, border=0, 
                                     command=self.refresh_to_do_list, bg=self.LIGHT_COLOR, 
                                     activebackground=self.LIGHT_COLOR)
        self.trash_icon = ImageTk.PhotoImage(Image.open("icons/trash_icon.png"))
        self.trash_button = Button(self.frame, image=self.trash_icon, border=0, 
                                   command=self.trash_to_do_list, bg=self.LIGHT_COLOR, 
                                   activebackground=self.LIGHT_COLOR)
        self.add_task_input = Entry(self.frame, width=20, font=self.ACTIVE_TASK_FONT, 
                                    justify= CENTER)

    def toggle_frame(self): 
        self.open_to_do.place_forget()
        # Place the to do list frame on the root window and buttons in the frame.
        self.frame.place(x=0,y=0)
        self.close_to_do.place(x=250,y=10)
        self.add_task_button.place(x=50,y=430)
        self.refresh_button.place(x=125,y=430)
        self.trash_button.place(x=200,y=430)

        # If there are no tasks saved, retrieve them from the to do list csv.
        if not self.active_tasks and not self.completed_tasks and not self.queued_tasks:
            self.get_task_list()
        else:
            self.place_current_tasks()

        self.window.bind('<t>', (lambda event: self.close_task_list()))


    def get_task_list(self):
        y = 40
        df = pandas.read_csv('ToDoList.csv')
        for index, row in df.iterrows():
            # For the first 10 tasks in the csv, create a button and place it on the to do list frame.
            if index < 10:
                button = self.create_task_button(row["Task"])
                button.place(x=10, y=y, anchor='w')
                y += 40
            # After the first 10 tasks, queue them to be placed or saved later.
            else:
                self.queued_tasks[row['Task']] = None
 
    def place_current_tasks(self):
    # This method places all saved active and completed tasks in the frame.
        
        y = 40
        # Start by placing the active tasks.
        for task, button in self.active_tasks.items():
                button.place(x=10, y=y, anchor='w')
                y += 40
        # Then place the completed tasks.
        for task, button in self.completed_tasks.items():
                button.place(x=10, y=y, anchor='w')
                y += 40

    def create_task_button(self, task):
        new_button = Button(self.frame,text=task,
                            font= self.ACTIVE_TASK_FONT,
                            justify= LEFT,
                            wraplength=250,
                            fg=self.DARK_COLOR,
                            border=0,
                            bg=self.LIGHT_COLOR,
                            activeforeground=self.DARK_COLOR,
                            activebackground=self.LIGHT_COLOR)
        new_button.config(command=lambda b = new_button, t = task: self.cross_off_task(b,t))

        self.active_tasks[task] = new_button
        return new_button
    
    def cross_off_task(self, button, task):
        button.config(font=self.FINISHED_TASK_FONT, 
                      command= lambda b = button, t = task: self.uncross_off_task(b,t))
        # Move task from active to completed
        self.completed_tasks[task] = button
        del self.active_tasks[task]

    def uncross_off_task(self, button, task):
        button.config(font=self.ACTIVE_TASK_FONT, 
                      command= lambda b = button, t = task: self.cross_off_task(b,t))
        # Move task from completed to active
        self.active_tasks[task] = button
        del self.completed_tasks[task]
 
    def add_task(self):
    # This method reconfigures the screen to take input to add a new task.
        
        # Remove trash and reset button, move the add button, and place the entry bar.
        self.trash_button.place_forget()
        self.refresh_button.place_forget()
        self.add_task_input.place(x=75,y=435)
        self.add_task_button.place(x=30,y=430)
        
        # Reconfig the add button to save the task.
        self.add_task_button.config(command=self.save_task)
        self.add_task_input.bind('<Return>', (lambda event: self.save_task()))
   
    def save_task(self):  
        new_task = self.add_task_input.get()
        task_list_len = len(self.active_tasks) + len(self.completed_tasks)
        # If there is room on the frame, add a new button.
        if task_list_len < 10:
            self.active_tasks[new_task] = self.create_task_button(new_task)
        # If not, queue the task.
        else:
            self.queued_tasks[new_task] = None

        self.place_current_tasks()

        # Reset the to do list frame and buttons.
        self.add_task_input.place_forget()
        self.add_task_input.delete(0, END)
        self.add_task_input.unbind('<Return>')
        self.refresh_button.place(x=125,y=430)
        self.trash_button.place(x=200,y=430)
        self.add_task_button.place(x=50,y=430)
        self.add_task_button.config(command=self.add_task)
    
    def refresh_to_do_list(self):
        result = mb.askquestion('Refresh To Do List', 
                                'Are you sure you want to refresh?\n\nDoing so will delete all completed tasks.')
        if result == 'yes':
            # Move the active tasks to the top of the frame
            self.place_current_tasks()
            self.clear_tasks_from_frame(self.completed_tasks)
            self.completed_tasks = {}

    def trash_to_do_list(self):
        result = mb.askquestion('Trash To Do List', 'Are you sure you want to trash all tasks?')

        if result == 'yes':
            self.clear_tasks_from_frame(self.active_tasks, self.completed_tasks)
            self.completed_tasks = {}
            self.active_tasks = {}
            self.queued_tasks = {}

    def clear_tasks_from_frame(self, dict1, dict2 = None):
        for task in dict1.keys():
            dict1[task].place_forget()
        if dict2:
            for task in dict2.keys():
                dict2[task].place_forget()

    def close_task_list(self):
        self.frame.place_forget()
        self.open_to_do.place(x=5,y=10)
        self.window.bind('<t>', (lambda event: self.toggle_frame()))

    def update_csv(self):
        remaining_tasks = {'Task': []}

        for task in self.active_tasks.keys():
            remaining_tasks['Task'].append(task)
            
        for task in self.queued_tasks.keys():
            remaining_tasks['Task'].append(task)

        df = pandas.DataFrame(remaining_tasks)
        df.to_csv('ToDoList.csv', index=False)