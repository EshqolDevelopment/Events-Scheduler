import os
from actions.base_task import BaseTask
import tkinter as tk
from tkinter import filedialog


def file_dialog():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()


class OpenApp(BaseTask):
    action = "Open App"

    def config(self, gui):
        chosen_file = file_dialog()
        if chosen_file:
            gui.open_task_config(self.action, {"app_path": chosen_file})

    def run(self, content: dict[str, str]):
        os.startfile(content["app_path"])
