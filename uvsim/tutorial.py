import tkinter as tk 
from tkinter import messagebox as mb
from PIL import ImageTk, Image
import os

class HelpMenu():
    def __init__(self, master:tk.Tk)->None:
        FONT = None
        width = 13
        self.master = master

        self.master.geometry("600x400")
        self.master.title("Help Menu") 
        self.master.configure()
    
        self.master_frame = tk.Frame(self.master)
        self.master_frame.columnconfigure((0,4), weight=1)
        self.master_frame.rowconfigure(index=0, weight=3)
        self.master_frame.rowconfigure(index=2, weight=1)
        
        self.upper_frame = tk.Frame(self.master_frame)
        self.upper_frame.grid(column=0,row=0, sticky="n",padx=3, pady=3)

        self.image_list = self.open_images()
        self.image_count = len(self.image_list)
        self.image_iter = iter(self.image_list)
        self.current_image = tk.Label(self.upper_frame, image=next(self.image_iter))
        self.current_image.grid(column=0, row=0, sticky='n', padx=3, pady= 3)

        self.lower_frame = tk.Frame(self.master_frame) 
        self.lower_frame.grid(column=0,row=2, sticky="s",padx=3, pady=3)

        self.bttns = [
            tk.Button(self.lower_frame, font= FONT, command=self.get_next, width=width, text="Next"),
            tk.Button(self.lower_frame, font=FONT, command=exit, width=width, text ="exit")
        ]

        for idx, ele in enumerate(self.bttns,2):
            ele.grid(row=4, column=idx, sticky='se', padx=50, pady=20) 

        self.master_frame.pack(fill="both", expand=True)


    def get_next(self):
        try:
            self.current_image.config(image=next(self.image_iter))
        except StopIteration:
            exit()
            
    def open_images(self) -> [str]:
        lyst = [ImageTk.PhotoImage(Image.open(os.path.join(r"uvsim\tutorial_images",filepath))) for filepath in os.listdir(r'uvsim\tutorial_images')] 
        return lyst
        