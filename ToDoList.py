# This class is inspired by PROGRAMMED on YouTube. https://www.youtube.com/watch?v=COQ-T3qZkoA

from tkinter import *
from PIL import ImageTk,Image

class ToDoList:
    def __init__(self, window):
        self.w = window
        self.img1 = ImageTk.PhotoImage(Image.open("open.png"))
        self.open_to_do = Button(self.w, image=self.img1, command=self.toggle_win, border=0, bg='#040D12', activebackground='#183D3D')
        self.open_to_do.place(x=5,y=10)
        

    def toggle_win(self):
        self.open_to_do.place_forget()
        self.f1 = Frame(self.w,width=300,height=500,bg='#5C8374')
        self.f1.place(x=0,y=0)
        self.img2 = ImageTk.PhotoImage(Image.open("close.png"))
        self.close_to_do = Button(self.f1, image=self.img2, border=0, command=self.dele, bg='#5C8374', activebackground='#5C8374')
        self.close_to_do.place(x=5,y=10)


        #buttons
        def bttn(x,y,text,bcolor,fcolor,cmd):
     
            def on_entera(e):
                myButton1['background'] = bcolor #ffcc66
                myButton1['foreground']= '#262626'  #000d33

            def on_leavea(e):
                myButton1['background'] = fcolor
                myButton1['foreground']= '#262626'

            myButton1 = Button(self.f1,text=text,
                           width=42,
                           height=2,
                           fg='#262626',
                           border=0,
                           bg=fcolor,
                           activeforeground='#262626',
                           activebackground=bcolor,            
                            command=cmd)
                      
            myButton1.bind("<Enter>", on_entera)
            myButton1.bind("<Leave>", on_leavea)

            myButton1.place(x=x,y=y)

        bttn(0,80,'A C E R','#5C8374','#5C8374',None)
        bttn(0,117,'D E L L','#5C8374','#5C8374',None)
        bttn(0,154,'A P P L E','#5C8374','#5C8374',None)
        bttn(0,191,'A S U S','#5C8374','#5C8374',None)
        bttn(0,228,'A C E R','#5C8374','#5C8374',None)
        bttn(0,265,'A C E R','#5C8374','#5C8374',None)


    def dele(self):
        self.f1.place_forget()
        self.open_to_do.place(x=5,y=10)


        