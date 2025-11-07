import tkinter as tk
from tkinter import filedialog, ttk
import os
import fileLooper

class appGui(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Tiktok Ending Detecter & Remover")
        self.geometry("500x500")
        
        self.appUi()
    
    def appUi(self):

        toolbar = tk.Frame(self, bg="#1e1e1e")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        def buttonBuilder(text, cmd):
            button = tk.Button(toolbar, text=text, command=cmd)
            button.pack(side=tk.TOP, padx=4, pady=4)

        buttonBuilder(text="Choose dir", cmd=self.chooseDirectory)
    
        self.appResponse = tk.Label(self, text="Work In Progress!", font=("Arial, 20"))
        self.appResponse.pack()

    def chooseDirectory(self):
        convResponse = fileLooper.fileLooper(filedialog.askdirectory())   


app = appGui()
app.mainloop()