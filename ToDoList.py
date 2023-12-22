from tkinter import *
from tkinter import messagebox as mb
from PIL import ImageTk,Image
import pandas

class ToDoList:
    def __init__(self, window):
        self.w = window
        self.img1 = ImageTk.PhotoImage(Image.open("icons/list_icon.png"))
        self.open_to_do = Button(self.w, image=self.img1, command=self.toggle_win, border=0, bg="#272829", activebackground="#272829")
        self.open_to_do.place(x=10,y=15)
        self.active_tasks = {}
        self.completed_tasks = {}
        self.queued_tasks = {}
        self.active_task_font = ("Courier", 12, "bold")
        self.finished_task_font = ("Courier", 12, "overstrike")

        self.f1 = Frame(self.w,width=300,height=500,bg='#5C8374')
        self.img2 = ImageTk.PhotoImage(Image.open("icons/close_icon.png"))
        self.close_to_do = Button(self.f1, image=self.img2, border=0, command=self.close_task_list, bg='#5C8374', activebackground='#5C8374')
        self.img3 = ImageTk.PhotoImage(Image.open("icons/add_icon.png"))
        self.add_task_button = Button(self.f1, image=self.img3, border=0, command=self.add_task, bg='#5C8374', activebackground='#5C8374')
        self.img4 = ImageTk.PhotoImage(Image.open("icons/refresh_icon.png"))
        self.refresh_button = Button(self.f1, image=self.img4, border=0, command=self.refresh_to_do_list, bg='#5C8374', activebackground='#5C8374')
        self.img5 = ImageTk.PhotoImage(Image.open("icons/trash_icon.png"))
        self.trash_button = Button(self.f1, image=self.img5, border=0, command=self.trash_to_do_list, bg='#5C8374', activebackground='#5C8374')
        self.add_task_input = Entry(self.f1, width=20, font=self.active_task_font, justify= CENTER)

    def toggle_win(self):
        self.open_to_do.place_forget()
        
        self.f1.place(x=0,y=0)
        self.close_to_do.place(x=250,y=10)
        self.add_task_button.place(x=50,y=430)
        self.refresh_button.place(x=125,y=430)
        self.trash_button.place(x=200,y=430)

        if not self.active_tasks and not self.completed_tasks and not self.queued_tasks:
            self.get_task_list()
        else:
            self.place_current_tasks()


    def get_task_list(self):
        x = 10
        y = 40
        df = pandas.read_csv('ToDoList.csv')

        for index, row in df.iterrows():
            if index < 10:
                button = self.create_task_button(row["Task"])
                button.place(x=10, y=y, anchor='w')
                y += 40
            else:
                self.queued_tasks[row['Task']] = None

    def place_current_tasks(self):
        y = 40
        for task, button in self.active_tasks.items():
                button.place(x=10, y=y, anchor='w')
                y += 40
        for task, button in self.completed_tasks.items():
                button.place(x=10, y=y, anchor='w')
                y += 40

    def create_task_button(self, task):
        new_button = Button(self.f1,text=task,
                            font= self.active_task_font,
                            justify= LEFT,
                            wraplength=250,
                            fg='#272829',
                            border=0,
                            bg='#5C8374',
                            activeforeground='#272829',
                            activebackground='#5C8374')
        new_button.config(command=lambda b = new_button, t = task: self.cross_off_task(b,t))
        self.active_tasks[task] = new_button
        return new_button
    
    def cross_off_task(self, button, task):
        button.config(font=self.finished_task_font, command= lambda b = button, t = task: self.uncross_off_task(b,t))
        self.completed_tasks[task] = button
        del self.active_tasks[task]

    def uncross_off_task(self, button, task):
        button.config(font=self.active_task_font, command= lambda b = button, t = task: self.cross_off_task(b,t))
        self.active_tasks[task] = button
        del self.completed_tasks[task]

    def add_task(self):
        self.trash_button.place_forget()
        self.refresh_button.place_forget()
        self.add_task_input.place(x=75,y=435)
        self.add_task_button.config(command=self.save_task)
        self.add_task_button.place(x=30,y=430)
        self.add_task_input.bind('<Return>', (lambda event: self.save_task()))

        
    def save_task(self):
        new_task = self.add_task_input.get()
        task_list_len = len(self.active_tasks) + len(self.completed_tasks)

        if task_list_len < 10:
            self.active_tasks[new_task] = self.create_task_button(new_task)
        else:
            self.queued_tasks[new_task] = None

        self.place_current_tasks()

        self.add_task_input.place_forget()
        self.add_task_input.unbind('<Return>')
        self.refresh_button.place(x=125,y=430)
        self.trash_button.place(x=200,y=430)
        self.add_task_button.place(x=50,y=430)
        self.add_task_button.config(command=self.add_task)

    def update_csv(self):
        remaining_tasks = {'Task': []}
        for task in self.active_tasks.keys():
            remaining_tasks['Task'].append(task)
        for task in self.queued_tasks.keys():
            remaining_tasks['Task'].append(task)
        df = pandas.DataFrame(remaining_tasks)
        df.to_csv('ToDoList.csv', index=False)

    def clear_tasks(self, dict1, dict2 = None, dict3 = None):
        for task in dict1.keys():
            dict1[task].place_forget()
        if dict2:
            for task in dict2.keys():
                dict2[task].place_forget()
        if dict3:
            for task in dict3.keys():
                dict3[task].place_forget()
    def close_task_list(self):
        self.f1.place_forget()
        self.open_to_do.place(x=5,y=10)
    
    def refresh_to_do_list(self):
        result = mb.askquestion('Refresh To Do List', 'Are you sure you want to refresh?\n\nDoing so will delete all completed tasks.')
        if result == 'yes':
            self.place_current_tasks()
            self.clear_tasks(self.completed_tasks)
            self.completed_tasks = {}

    def trash_to_do_list(self):
        result = mb.askquestion('Trash To Do List', 'Are you sure you want to trash all tasks?')
        if result == 'yes':
            self.clear_tasks(self.active_tasks, self.completed_tasks, self.queued_tasks)
            self.completed_tasks = {}
            self.active_tasks = {}
            self.queued_tasks = {}