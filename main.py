import socket
import sys

from kivy.clock import mainthread

APP_NAME = "Events Scheduler Pro"

if sys.platform != "darwin":
    try:
        s = socket.socket()
        host = socket.gethostname()
        port = 12382
        s.bind((host, port))
    except Exception:
        try:
            import win32com.client
            import win32con
            import win32gui

            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            HWND = win32gui.FindWindowEx(0, 0, 0, APP_NAME)
            win32gui.ShowWindow(HWND, win32con.SW_RESTORE)
            win32gui.SetWindowPos(HWND, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
            win32gui.SetWindowPos(HWND, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
            win32gui.SetWindowPos(HWND, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
            win32gui.SetForegroundWindow(HWND)
            sys.exit()
        except Exception:
            sys.exit()

from kivymd.uix.list import ThreeLineAvatarIconListItem, IconLeftWidget, ThreeLineListItem, IconRightWidget
from kivy4 import *
from kv import *
import tkinter as tk
from tkinter import filedialog
from task import Task
from task_config import TaskConfig
from time_operations import reformat_extend_date
from actions import action_dict

spacer = " " * 25


class App(Kivy4):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action_to_icon = {k: v["icon"] for k, v in action_dict.items()}
        self.save_popup = None
        self.current_task_config = None
        self.tasks_dict: dict[str, Task] = {}

    def on_start(self):
        item = ThreeLineListItem(text="Here you can create and edit your tasks",
                                 secondary_text="Press on the + to add a new task to the list",
                                 tertiary_text="Delete a task by pressing on the trash icon on the right")
        self.ids.container.add_widget(item)
        self.create_tasks_list()

        first_run = self.get_file("first_run", default="True")

        if first_run == "True":
            self.open_info_popup()

    def create_tasks_list(self):
        tasks = self.get_files_content("Tasks", is_json=True)
        for task_dict in tasks:
            task_dict["next_run_time"] = task_dict.get("next_run_time")
            self.add_task(Task(**task_dict))

    def open_task_config(self, action: str, content: dict[str, str], task: Task = None):
        self.current_task_config = TaskConfig(action, content, self, task)

    def add_task(self, task: Task):
        next_run_time = task.calculate_next_run_time()
        item = ThreeLineAvatarIconListItem(text=f"{spacer}[b]{task.name}[/b]",
                                           secondary_text=f"{spacer}Action: {task.action}",
                                           tertiary_text=f"{spacer}[b]Next run:[/b] {reformat_extend_date(next_run_time)}")
        item.add_widget(IconRightWidget(icon=self.action_to_icon[task.action]))
        item.add_widget(IconLeftWidget(icon="delete-outline", on_release=lambda *args: self.open_delete_task_dialog(task)))
        item.add_widget(IconLeftWidget(icon="pencil-outline", on_release=lambda *args: self.open_edit_task_dialog(task)))
        item.add_widget(IconLeftWidget(icon="play-circle-outline", on_release=lambda *args: task.run_task()))

        self.ids.container.add_widget(item)
        task.schedule_task(self)
        self.tasks_dict[task.name] = task

    def open_edit_task_dialog(self, task: Task):
        self.open_task_config(task.action, task.content, task)

    def find_row_by_task(self, name: str):
        for row in self.ids.container.children:
            if row.text == f"{spacer}[b]{name}[/b]":
                return row

    def update_task_row(self, task: Task):
        next_run_time = task.calculate_next_run_time()
        row = self.find_row_by_task(task.name)
        row.text = f"{spacer}[b]{task.name}[/b]"
        row.secondary_text = f"{spacer}Action: {task.action}"
        row.tertiary_text = f"{spacer}[b]Next run:[/b] {reformat_extend_date(next_run_time)}"

    def open_delete_task_dialog(self, task: Task):
        delete_task_popup = type("DeleteTask", (BoxLayout,), {})()
        self.popup_kivy4(title="Delete Task",
                         content=delete_task_popup,
                         okay_text="Delete",
                         cancel_text="Cancel",
                         okay_func=lambda *args: self.delete_task(task))

    @mainthread
    def delete_task(self, task: Task):
        self.delete_file(f"Tasks/{task.id}.json")
        self.dismiss()
        item = self.find_row_by_task(task.name)
        self.ids.container.remove_widget(item)
        self.tasks_dict[task.name].stop()
        self.tasks_dict.pop(task.name)

    def callback(self, row):
        reverse_action_dict = {self.action_to_icon[key]: key for key in self.action_to_icon}
        action = reverse_action_dict[row.icon]
        action_dict[action]["class"].config(self)

    def on_request_close(self, disable_x: bool = True):
        Window.hide()
        return True

    @staticmethod
    def parse_repeat_text(days, hours, minutes):
        days = days if days else "0"
        hours = hours if hours else "0"
        minutes = minutes if minutes else "0"

        try:
            days = int(days)
            minutes = int(minutes)
            hours = int(hours)
            if not (days or hours or minutes):
                return "Run once at the start date"

            return f"Repeat every {days} days, {hours} hours and {minutes} minutes"
        except Exception:
            return "Invalid inputs"

    def open_info_popup(self, *_):
        def okay_func(*_):
            self.set_file("first_run", "False")
            self.dismiss()

        welcome_popup = type("Welcome", (BoxLayout,), {})()
        self.popup_kivy4(title="Welcome to Events Scheduler Pro",
                         content=welcome_popup,
                         okay_text="Got it",
                         cancel_text="",
                         okay_func=okay_func)


def file_dialog():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()


if __name__ == '__main__':
    App(app_name=APP_NAME, string=kiv, app_data=True, main_color='Orange', pre_string=pre,
        toolbar=['[["information-variant", app.open_info_popup]]',
                 '[[app.dark_mode_icon, lambda x: app.reverse_dark_mode()]]'],
        list_of_dirs=["Tasks"], icon="icon.png").run()
