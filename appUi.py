import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
import queue

import endingRemover
import fileLooper


# noinspection PyTypeChecker
class AppGui(tk.Tk):
    def __init__(self):
        super().__init__()

        # init the queue for progressbar purposes
        self.queue_progressbar = queue.Queue()

        self.chosen_dir_input = None
        self.chosen_dir_output = None
        self.amount_of_files = None
        self.progressbar_progress = None

        self.answer_text = tk.StringVar()
        self.skip_original_string = tk.BooleanVar()
        self.keep_original_video = tk.BooleanVar()
        self.same_output_dir_var = tk.BooleanVar()

        self.title("Tiktok Ending Detecter & Remover")
        self.geometry("1280x720")
        
        self.app_ui()
        self.start_button.config(state = tk.DISABLED)
    
    def app_ui(self):

        toolbar = tk.Frame(self, bg="#1e1e1e")
        toolbar.pack(side = tk.TOP, fill = tk.X)

        self.choose_dir_button = tk.Button(toolbar, text = "Choose work dir", command = self.choose_input_directory)
        self.choose_dir_button.pack(side = tk.LEFT, padx = 4, pady = 4)

        self.choose_output_dir_button = tk.Button(toolbar, text="Choose output dir", command = self.choose_output_directory)
        self.choose_output_dir_button.pack(side=tk.LEFT, padx=4, pady=4)

        self.start_button = ttk.Button(self, text = "Start conversion", command = self.start_conversion)
        self.start_button.pack(side=tk.TOP, padx=4, pady=4)

        self.check_org_video = ttk.Checkbutton(self, text = "Keep Original Video", variable = self.keep_original_video)
        self.check_org_video.pack(side=tk.TOP, padx=4, pady=4)

        self.skip_original_button = ttk.Checkbutton(self, text = "Skip video if it was already checked and has original in name", variable = self.skip_original_string)
        self.skip_original_button.pack(side=tk.TOP, padx=4, pady=4)

        self.same_output_dir_button = ttk.Checkbutton(self, text = "Use the same output dir as the working one", variable = self.same_output_dir_var, command = self.check_if_can_start)
        self.same_output_dir_button.pack(side=tk.TOP, padx=4, pady=4)

        self.app_response = tk.Label(self, textvariable = self.answer_text, font = "Arial, 16")
        self.app_response.pack(pady = 50)

        self.file_work_progress_text = ttk.Label(self, text = "Progress of checking videos: ", font = "Arial, 16")
        self.file_work_progress_text.pack()

        self.file_work_progress = ttk.Progressbar(self, orient = "horizontal", length = 500, mode = "determinate")
        self.file_work_progress.pack()

    def check_if_can_start(self):
        self.same_output_dir_value = self.same_output_dir_var.get()

        # we check if the input dir was chosen before allowing to start
        if self.same_output_dir_value and self.chosen_dir_input != "()" and self.chosen_dir_input != "" and self.chosen_dir_input is not None:
            self.start_button.config(state = tk.NORMAL)
        else:
            self.start_button.config(state = tk.DISABLED)

        # we check if the output dir was chosen before allowing to start (if user wants to output files to another dir in the first place)
        if not self.same_output_dir_value and self.chosen_dir_output != "()" and self.chosen_dir_output != "" and self.chosen_dir_output is not None:
            self.start_button.config(state = tk.NORMAL)
        elif not self.same_output_dir_value:
            self.start_button.config(state = tk.DISABLED)

        # disabling output dir choice we button of same input is clicked
        if self.same_output_dir_value:
            self.choose_output_dir_button.config(state = tk.DISABLED)
        else:
            self.choose_output_dir_button.config(state = tk.NORMAL)

    def choose_input_directory(self):
        # disable start button until a valid path is chosen by a user
        self.chosen_dir_input = filedialog.askdirectory()
        self.check_if_can_start()

    def start_conversion(self):
        try:
            self.start_button.config(state = tk.DISABLED)
            self.keep_original_value = self.keep_original_video.get()
            self.skip_original_value = self.skip_original_string.get()
            self.amount_of_files = fileLooper.files_count(self.chosen_dir_input)
            self.file_work_progress.config(maximum=self.amount_of_files)
            self.same_output_dir_value = self.same_output_dir_var.get()

            if self.same_output_dir_value:
                self.what_output_dir = self.chosen_dir_input
            else:
                self.what_output_dir = self.chosen_dir_output

            threaded_progress = threading.Thread(target=fileLooper.loop_through_files,
                                                 args=(self.chosen_dir_input, self.keep_original_value,
                                                       self.skip_original_value, self.queue_progressbar,
                                                       self.same_output_dir_value, self.what_output_dir))

            threaded_progress.start()
            self.retrieve_data_progressbar()

        except endingRemover.RemovalError:
            self.app_response.config(fg="red")
            self.answer_text.set("ERROR: The app can't convert your videos because to lack of permissions.")
        except endingRemover.ConversionError as e:
            self.app_response.config(fg="red")
            self.answer_text.set(f"ERROR: The app can't convert your videos because of: {e}")
        except PermissionError as e:
            self.app_response.config(fg="red")
            self.answer_text.set(f"{e}")
        except fileLooper.NotStringError as e:
            self.answer_text.set("")
        except fileLooper.InvalidPathError as e:
            self.answer_text.set("")

    def choose_output_directory(self):
        self.chosen_dir_output = filedialog.askdirectory()
        self.check_if_can_start()

    def same_output_dir(self):
        self.same_output_dir_value = self.same_output_dir_var.get()
        if self.same_output_dir_value:
            self.choose_output_dir_button.config(state = tk.DISABLED)
        else:
            self.choose_output_dir_button.config(state = tk.NORMAL)

    def retrieve_data_progressbar(self):
        try:
            self.progressbar_progress = self.queue_progressbar.get_nowait()

            if isinstance(self.progressbar_progress, int):
                self.file_work_progress_text.config(text=f"Progress of checking videos: {self.progressbar_progress} / {self.amount_of_files}")
                self.file_work_progress["value"] = self.progressbar_progress

            elif isinstance(self.progressbar_progress, dict):
                    self.file_work_progress_text.config(text = "Converting videos is done!")
                    self.app_response.config(fg="green")
                    self.answer_text.set(
                        f"SUCCESS: Amount of videos in your folder: {self.progressbar_progress["video_amount"]}\n"
                        f"Videos that endings got removed from: {self.progressbar_progress["video_with_ending_amount"]}")
                    self.start_button.config(state = tk.NORMAL)
                    return

        except queue.Empty:
            pass

        self.after(100, self.retrieve_data_progressbar)


app = AppGui()
app.mainloop()