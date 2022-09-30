from datetime import datetime, timedelta
from kivymd.uix.list import ThreeLineAvatarIconListItem, IconLeftWidget
from kivy4 import *
from kv import *


action_to_icon = {
    'Open App': 'launch',
    'System Command': 'console',
    'Send Email': 'email',
    'Python Command': 'language-python',
    'Open Website': 'web',
}


class SystemCommand(BoxLayout):
    pass


class SendEmail(BoxLayout):
    pass


class PythonCommand(BoxLayout):
    pass


class SavePopup(BoxLayout):
    pass


class TaskConfig:
    def __init__(self, action_name: str, content: dict[str, str], gui: "App"):
        self.save_popup = SavePopup()
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

        task = {
            "name": task_name,
            "action": self.action_name,
            "content": self.content,
            "start_date": self.start_date,
            "start_time": self.start_time,
            "repeat_every": repeat_every
        }

        self.gui.set_file(f"Tasks/{task_name}", task, is_json=True)
        self.gui.add_task(task)
        self.gui.dismiss()


class App(Kivy4):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action_dict = action_to_icon
        self.save_popup = None
        self.current_task_config = None

    def on_start(self):
        item = ThreeLineAvatarIconListItem(text="Here you can create and edit tasks",
                                           secondary_text="Press on the + to add step and save your task with the save icon",
                                           tertiary_text="Edit your existing task with the pen file icon at the top bar")
        item.add_widget(IconLeftWidget(icon="repeat"))
        self.ids.container.add_widget(item)
        self.create_tasks_list()

    def create_tasks_list(self):
        tasks = self.get_files_content("Tasks", is_json=True)
        for task in tasks:
            self.add_task(task)

    def calculate_next_run_time(self, start_date: str, start_time: str, repeat_every: dict[str, int]) -> datetime:
        start_date = datetime.strptime(start_date, "%d/%m/%Y")
        start_time = datetime.strptime(start_time, "%H:%M:%S")

        start_datetime = datetime.combine(start_date, start_time.time())
        repeat_every = timedelta(**repeat_every)
        return start_datetime + repeat_every

    @staticmethod
    def reformat_extend_date(next_run_time: datetime) -> str:
        return next_run_time.strftime("Date: %d/%m/%Y | Time: %H:%M:%S")

    def add_task(self, task: dict):
        next_run_time = self.calculate_next_run_time(task["start_date"], task["start_time"], task["repeat_every"])
        item = ThreeLineAvatarIconListItem(text=task["name"],
                                           secondary_text=f"Action: {task['action']}",
                                           tertiary_text=f"[b]Next run:[/b] {self.reformat_extend_date(next_run_time)}")
        item.add_widget(IconLeftWidget(icon=action_to_icon[task["action"]]))
        self.ids.container.add_widget(item)

    def callback(self, x):
        reverse_action_dict = {action_to_icon[key]: key for key in action_to_icon}
        action = reverse_action_dict[x.icon]

        if action == "System Command":
            cmd_popup = SystemCommand()
            self.popup_kivy4(title="Run System Command", content=cmd_popup,
                             okay_func=lambda *args: self.open_task_config(
                                 action,
                                 {"command": cmd_popup.ids.cmd_command_input.text}))

        elif action == "Send Email":
            email_popup = SendEmail()
            self.popup_kivy4(title="Send Email", content=email_popup,
                             okay_func=lambda *args: self.open_task_config(
                                 action,
                                 {"to": email_popup.ids.email_to_input.text,
                                  "subject": email_popup.ids.email_subject_input.text,
                                  "message": email_popup.ids.email_message_input.text}))

        elif action == "Python Command":
            python_popup = PythonCommand()
            self.popup_kivy4(title="Run Python Command", content=python_popup,
                             okay_func=lambda *args: self.open_task_config(
                                 action,
                                 {"command": python_popup.ids.python_command_input.text}))

        elif action == "Open App":
            # open file dialog
            self.file_dialog()

    @thread
    def file_dialog(self):
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()
        print(file_path)

    def open_task_config(self, action_name: str, content: dict[str, str]):
        self.current_task_config = TaskConfig(action_name, content, self)


if __name__ == '__main__':
    App(app_name='Events Scheduler', string=kiv, app_data=True, main_color='Orange', pre_string=pre, toolbar=True,
        list_of_dirs=["Tasks"]).run()
