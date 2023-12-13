from tkinter import *
from PIL import ImageTk,Image

class ToDoList:
    def __init__(self, window):
        self.w = window
        self.img1 = ImageTk.PhotoImage(Image.open("open.png"))
        self.open_to_do = Button(self.w, image=self.img1, command=self.toggle_win, border=0, bg='#040D12', activebackground='#183D3D')
        self.open_to_do.place(x=5,y=10)
        
        # self.active_task_font = font.Font(family="Courier", overstrike = 0)
        self.active_task_font = ("Courier", 12)
        self.finished_task_font = ("Courier", 12, "overstrike")

    def toggle_win(self):
        self.open_to_do.place_forget()
        self.f1 = Frame(self.w,width=300,height=500,bg='#5C8374')
        self.f1.place(x=0,y=0)
        self.img2 = ImageTk.PhotoImage(Image.open("close.png"))
        self.close_to_do = Button(self.f1, image=self.img2, border=0, command=self.dele, bg='#5C8374', activebackground='#5C8374')
        self.close_to_do.place(x=5,y=10)
        
        self.create_tasks()


    def create_tasks(self):
        x = 10
        y = 80
        tasks = ["sleep", "eat", "study"]
        

        for task in tasks:
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
            new_button.place(x=x, y=y, anchor='w')
            y += 40

    def cross_off_task(self, button):
        button.config(font=self.finished_task_font, command= lambda b = button: self.uncross_off_task(b))

    def uncross_off_task(self, button):
        button.config(font=self.active_task_font, command= lambda b = button: self.cross_off_task(b))

    def dele(self):
        self.f1.place_forget()
        self.open_to_do.place(x=5,y=10)


        