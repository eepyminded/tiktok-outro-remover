import tkinter as tk
from tkinter import filedialog, ttk
import os
import endingDetecter

class appGui(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Tiktok Ending Detecter & Remover")
        self.geometry("1280x720")
        
        self.appUi()

    def appUi(self):
        toolbar = tk.Frame(self, bg="#575353")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        def buttonBuilder(text, cmd):
            button = tk.Button(toolbar, text=text, command=cmd)
            button.pack(side=tk.LEFT, padx=4, pady=4)

        buttonBuilder(text="Choose dir")

app = appGui()
app.mainloop()