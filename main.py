import webbrowser
from dataclasses import dataclass
from datetime import datetime, timedelta
from kivymd.uix.list import ThreeLineAvatarIconListItem, IconLeftWidget, ThreeLineListItem, IconRightWidget
from kivy4 import *
from kv import *
import tkinter as tk
from tkinter import filedialog

action_to_icon = {
    'Open App': 'launch',
    'System Command': 'console',
    'Send Email': 'email',
    'Python Command': 'language-python',
    'Open Website': 'web',
}


@dataclass
class Task:
    name: str
    action: str
    content: dict[str, str]
    start_date: str
    start_time: str
    repeat_every: dict[str, int]
    next_run_time: str | None

    def calculate_next_run_time(self) -> datetime:
        if self.next_run_time is not None:
            return datetime.strptime(self.next_run_time, "Date: %d/%m/%Y | Time: %H:%M")

        start_date = datetime.strptime(self.start_date, "%d/%m/%Y")
        start_time = datetime.strptime(self.start_time, "%H:%M:%S")

        return datetime.combine(start_date, start_time.time())

    @thread
    def schedule_task(self, gui: "App"):
        next_run_time = self.calculate_next_run_time()

        while True:
            if self.next_run_time == "Stop":
                break
            if datetime.now() >= next_run_time:
                self.run_task()
                next_run_time = datetime.now() + timedelta(**self.repeat_every)
                self.next_run_time = gui.reformat_extend_date(next_run_time)
                gui.set_file(f"Tasks/{self.name}", self.__dict__, is_json=True)
                gui.update_task_row(self)

            time.sleep(1)

    def run_task(self):
        action = self.action
        content = self.content
        if action == "Open App":
            webbrowser.open(content["app_path"])
        elif action == "Open Website":
            webbrowser.open(content["url"])
        elif action == "System Command":
            os.system(content["command"])
        elif action == "Python Command":
            exec(content["command"])

    def stop(self):
        self.next_run_time = "Stop"


class TaskConfig:
    def __init__(self, action_name: str, content: dict[str, str], gui: "App"):
        self.save_popup = type("SavePopup", (BoxLayout,), {})()
        self.gui = gui
        self.content = content
        self.action_name = action_name
        self.start_date = None
        self.start_time = None

        self.gui.popup_kivy4(title="Save and Schedule Task",
                             content=self.save_popup,
                             okay_func=lambda *args: self.save_current_task(),
                             okay_text="Save and Schedule",
                             cancel_text="Cancel")

    @staticmethod
    def reformat_date(date: datetime.date):
        return date.strftime("%d/%m/%Y")

    @staticmethod
    def reformat_time(time_: datetime.time):
        return time_.strftime("%H:%M:%S")

    def pick_start_date(self):
        self.gui.show_date_picker(on_save=lambda *args: self.save_start_date(args[1]))

    def save_start_date(self, chosen_date: datetime.date):
        self.start_date = self.reformat_date(chosen_date)
        self.save_popup.ids.start_date.text = f"  Start Date: {self.start_date}"

    def pick_start_time(self):
        self.gui.show_time_picker(on_save=lambda *args: self.save_start_time(args[1]))

    def save_start_time(self, chosen_time: datetime.time):
        self.start_time = self.reformat_time(chosen_time)
        self.save_popup.ids.start_time.text = f"  Start Time: {self.start_time}"

    def save_current_task(self):
        task_name = self.save_popup.ids.save_name_input.text
        days = self.save_popup.ids.days_input.text
        hours = self.save_popup.ids.hours_input.text
        minutes = self.save_popup.ids.minutes_input.text
        repeat_every = {"days": int(days), "hours": int(hours), "minutes": int(minutes)}
        task = Task(task_name, self.action_name, self.content, self.start_date, self.start_time, repeat_every, None)

        self.gui.set_file(f"Tasks/{task_name}", task.__dict__, is_json=True)
        self.gui.add_task(task)
        self.gui.dismiss()


class App(Kivy4):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action_dict = action_to_icon
        self.save_popup = None
        self.current_task_config = None
        self.tasks_dict: dict[str, Task] = {}

    def on_start(self):
        item = ThreeLineListItem(text="Here you can create and edit tasks",
                                 secondary_text="Press on the + to add a new task to the list",
                                 tertiary_text="Edit and delete your existing task with the pencil icon")
        self.ids.container.add_widget(item)
        self.create_tasks_list()

    def create_tasks_list(self):
        tasks = self.get_files_content("Tasks", is_json=True)
        for task_dict in tasks:
            self.add_task(Task(**task_dict))

    @staticmethod
    def reformat_extend_date(next_run_time: datetime) -> str:
        return next_run_time.strftime("Date: %d/%m/%Y | Time: %H:%M")

    def open_task_config(self, action: str, content: dict[str, str]):
        self.current_task_config = TaskConfig(action, content, self)

    def add_task(self, task: Task):
        next_run_time = task.calculate_next_run_time()
        item = ThreeLineAvatarIconListItem(text=task.name,
                                           secondary_text=f"Action: {task.action}",
                                           tertiary_text=f"[b]Next run:[/b] {self.reformat_extend_date(next_run_time)}")
        item.add_widget(IconLeftWidget(icon=action_to_icon[task.action]))
        item.add_widget(
            IconRightWidget(icon="pencil-outline", on_release=lambda *args: self.open_edit_task_dialog(task)))
        self.ids.container.add_widget(item)
        task.schedule_task(self)
        self.tasks_dict[task.name] = task

    def find_row_by_task(self, task: Task):
        for row in self.ids.container.children:
            if row.text == task.name:
                return row

    def update_task_row(self, task: Task):
        next_run_time = task.calculate_next_run_time()
        row = self.find_row_by_task(task)
        row.secondary_text = f"Action: {task.action}"
        row.tertiary_text = f"[b]Next run:[/b] {self.reformat_extend_date(next_run_time)}"

    def open_edit_task_dialog(self, task: Task):
        edit_task_popup = type("EditTask", (BoxLayout,), {})()
        self.popup_kivy4(title="Delete Task",
                         content=edit_task_popup,
                         okay_text="Delete",
                         cancel_text="Cancel",
                         okay_func=lambda *args: self.delete_task(task))

    def delete_task(self, task: Task):
        self.delete_file(f"Tasks/{task.name}.json")
        self.dismiss()
        item = self.find_row_by_task(task)
        self.ids.container.remove_widget(item)
        self.tasks_dict[task.name].stop()
        self.tasks_dict.pop(task.name)

    def callback(self, row):
        reverse_action_dict = {action_to_icon[key]: key for key in action_to_icon}
        action = reverse_action_dict[row.icon]

        if action == "System Command":
            cmd_popup = type("SystemCommand", (BoxLayout,), {})()
            self.popup_kivy4(title="Run System Command", content=cmd_popup,
                             okay_func=lambda *args: self.open_task_config(
                                 action,
                                 {"command": cmd_popup.ids.cmd_command_input.text}))

        elif action == "Send Email":
            email_popup = type("SendEmail", (BoxLayout,), {})()
            self.popup_kivy4(title="Send Email", content=email_popup,
                             okay_func=lambda *args: self.open_task_config(
                                 action,
                                 {"to": email_popup.ids.email_to_input.text,
                                  "subject": email_popup.ids.email_subject_input.text,
                                  "message": email_popup.ids.email_message_input.text}))

        elif action == "Python Command":
            python_popup = type("PythonCommand", (BoxLayout,), {})()
            self.popup_kivy4(title="Run Python Command", content=python_popup,
                             okay_func=lambda *args: self.open_task_config(
                                 action, {"command": python_popup.ids.python_command_input.text}))

        elif action == "Open App":
            chosen_file = self.file_dialog()
            if chosen_file:
                self.open_task_config(action, {"app_path": chosen_file})

        elif action == "Open Website":
            website_popup = type("WebsitePopup", (BoxLayout,), {})()
            self.popup_kivy4(title="Open Website", content=website_popup,
                             okay_func=lambda *args: self.open_task_config(
                                 action, {"url": website_popup.ids.url_input.text}))

    @staticmethod
    def file_dialog():
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename()


if __name__ == '__main__':
    App(app_name='Events Scheduler', string=kiv, app_data=True, main_color='Orange', pre_string=pre, toolbar=True,
        list_of_dirs=["Tasks"]).run()
