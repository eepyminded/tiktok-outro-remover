import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import endingRemover
import fileLooper


# noinspection PyTypeChecker
class AppGui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.check_org_video = None
        self.keep_original_value = None
        self.answer_text = None
        self.app_response = None
        self.keep_original_video = tk.BooleanVar()
        self.title("Tiktok Ending Detecter & Remover")
        self.geometry("1280x720")
        
        self.app_ui()
    
    def app_ui(self):

        toolbar = tk.Frame(self, bg="#1e1e1e")
        toolbar.pack(side = tk.TOP, fill = tk.X)

        def button_builder(text, cmd):
            button = tk.Button(toolbar, text=text, command = cmd)
            button.pack(side = tk.TOP, padx = 4, pady = 4)

        button_builder(text = "Choose dir", cmd = self.choose_directory)

        self.check_org_video = ttk.Checkbutton(self, text = "Keep Original Video", variable = self.keep_original_video)
        self.check_org_video.pack(side=tk.TOP, padx=4, pady=4)

        self.answer_text = tk.StringVar()
        self.app_response = tk.Label(self, textvariable = self.answer_text, font = "Arial, 16")
        self.app_response.pack()

    def choose_directory(self):
        try:
            self.keep_original_value = self.keep_original_video.get()
            modules_response = fileLooper.loop_through_files(filedialog.askdirectory(), self.keep_original_value)
            self.app_response.config(fg="green")
            self.answer_text.set(f"SUCCESS: Amount of videos in your folder: {modules_response["video_amount"]}, videos that endings got removed from: {modules_response["video_with_ending_amount"]}")
        except endingRemover.RemovalError:
            self.app_response.config(fg="red")
            self.answer_text.set("ERROR: The app can't convert your videos because to lack of permissions.")
        except endingRemover.ConversionError as e:
            self.app_response.config(fg="red")
            self.answer_text.set(f"ERROR: The app can't convert your videos because of: {e}")
        except PermissionError as e:
            self.app_response.config(fg="red")
            self.answer_text.set(f"{e}")

        # sometimes filedialog returns weird paths even when clicking cancel, we handle it quietly
        except fileLooper.NotStringError as e:
            self.answer_text.set("")
        except fileLooper.InvalidPathError as e:
            self.answer_text.set("")
        except:
            self.app_response.config(fg="red")
            self.answer_text.set(f"An unexpected error occurred")

app = AppGui()
app.mainloop()