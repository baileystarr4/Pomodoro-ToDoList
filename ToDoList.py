from tkinter import *
from PIL import ImageTk,Image
import pandas
from collections import defaultdict

class ToDoList:
    def __init__(self, window):
        self.w = window
        self.img1 = ImageTk.PhotoImage(Image.open("icons/list_icon.png"))
        self.open_to_do = Button(self.w, image=self.img1, command=self.toggle_win, border=0, bg="#272829", activebackground="#272829")
        self.open_to_do.place(x=10,y=10)
        self.tasks = defaultdict(None)
        
        # self.active_task_font = font.Font(family="Courier", overstrike = 0)
        self.active_task_font = ("Courier", 12)
        self.finished_task_font = ("Courier", 12, "overstrike")

    def toggle_win(self):
        self.open_to_do.place_forget()
        self.f1 = Frame(self.w,width=300,height=500,bg='#5C8374')
        self.f1.place(x=0,y=0)

        self.img2 = ImageTk.PhotoImage(Image.open("icons/close_icon.png"))
        self.close_to_do = Button(self.f1, image=self.img2, border=0, command=self.dele, bg='#5C8374', activebackground='#5C8374')
        self.close_to_do.place(x=250,y=10)

        self.img3 = ImageTk.PhotoImage(Image.open("icons/add_icon.png"))
        self.add_task_button = Button(self.f1, image=self.img3, border=0, command=self.dele, bg='#5C8374', activebackground='#5C8374')
        self.add_task_button.place(x=50,y=430)

        self.img4 = ImageTk.PhotoImage(Image.open("icons/refresh_icon.png"))
        self.refresh_button = Button(self.f1, image=self.img4, border=0, command=self.refresh_to_do_list, bg='#5C8374', activebackground='#5C8374')
        self.refresh_button.place(x=120,y=430)

        self.img5 = ImageTk.PhotoImage(Image.open("icons/trash_icon.png"))
        self.trash_button = Button(self.f1, image=self.img5, border=0, command=self.trash_to_do_list, bg='#5C8374', activebackground='#5C8374')
        self.trash_button.place(x=190,y=430)
        
        self.initialize_task_list()


    def initialize_task_list(self):
        x = 10
        y = 40
        df = pandas.read_csv('ToDoList.csv')

        for index, row in df.iterrows():
            if index < 10:
                self.create_task_button(row["Task"], y)
                y += 40
            else:
                self.tasks[row['Task']] = None

    def create_task_button(self, task, y):
        new_button = Button(self.f1,text=task,
                            font= self.active_task_font,
                            justify= LEFT,
                            wraplength=250,
                            fg='#040D12',
                            border=0,
                            bg='#5C8374',
                            activeforeground='#040D12',
                            activebackground='#5C8374')
        new_button.config(command=lambda b = new_button: self.cross_off_task(b))
        new_button.place(x=10, y=y, anchor='w')
        self.tasks[task] = new_button

    def cross_off_task(self, button):
        button.config(font=self.finished_task_font, command= lambda b = button: self.uncross_off_task(b))

    def uncross_off_task(self, button):
        button.config(font=self.active_task_font, command= lambda b = button: self.cross_off_task(b))
    
    def update_csv(self):
        remaining_tasks = {'Task': []}
        for task, button in self.tasks.items():
            if not button or "overstrike" not in button.cget("font"):
                remaining_tasks['Task'].append(task)
        df = pandas.DataFrame(remaining_tasks)
        df.to_csv('ToDoList.csv', index=False)

    def dele(self):
        self.f1.place_forget()
        self.open_to_do.place(x=5,y=10)
        self.update_csv()

    def add_task(self, task):
        # need to add input 
        task_list_len = len(self.tasks)
        if task_list_len < 10:
            y = task_list_len * 40
            self.create_task_button(task, y)
        else:
            self.tasks[task] = None
    
    def refresh_to_do_list(self):
        # need to add an "are you sure" pop up
        self.dele()
        self.toggle_win()

    def trash_to_do_list(self):
        # need to add an "are you sure" pop up
        self.tasks = defaultdict(None)
        self.dele()
        self.toggle_win()