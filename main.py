from kivymd.uix.list import ThreeLineAvatarIconListItem, IconLeftWidget, ThreeLineListItem, IconRightWidget
from kivy4 import *
from kv import *
import tkinter as tk
from tkinter import filedialog
from task import Task
from task_config import TaskConfig
from time_operations import reformat_extend_date

action_to_icon = {
    'Open App': 'launch',
    'System Command': 'console',
    'Send Email': 'email',
    'Python Command': 'language-python',
    'Open Website': 'web',
}


class App(Kivy4):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action_to_icon = action_to_icon
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

    def open_task_config(self, action: str, content: dict[str, str]):
        self.current_task_config = TaskConfig(action, content, self)

    def add_task(self, task: Task):
        next_run_time = task.calculate_next_run_time()
        item = ThreeLineAvatarIconListItem(text=f"[b]{task.name}[/b]",
                                           secondary_text=f"Action: {task.action}",
                                           tertiary_text=f"[b]Next run:[/b] {reformat_extend_date(next_run_time)}")
        item.add_widget(IconLeftWidget(icon=action_to_icon[task.action]))
        item.add_widget(
            IconRightWidget(icon="pencil-outline", on_release=lambda *args: self.open_edit_task_dialog(task)))
        self.ids.container.add_widget(item)
        task.schedule_task(self)
        self.tasks_dict[task.name] = task

    def find_row_by_task(self, task: Task):
        for row in self.ids.container.children:
            if row.text == f"[b]{task.name}[/b]":
                return row

    def update_task_row(self, task: Task):
        next_run_time = task.calculate_next_run_time()
        row = self.find_row_by_task(task)
        row.secondary_text = f"Action: {task.action}"
        row.tertiary_text = f"[b]Next run:[/b] {reformat_extend_date(next_run_time)}"

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
            chosen_file = file_dialog()
            if chosen_file:
                self.open_task_config(action, {"app_path": chosen_file})

        elif action == "Open Website":
            website_popup = type("WebsitePopup", (BoxLayout,), {})()
            self.popup_kivy4(title="Open Website", content=website_popup,
                             okay_func=lambda *args: self.open_task_config(
                                 action, {"url": website_popup.ids.url_input.text}))


def file_dialog():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()


if __name__ == '__main__':
    App(app_name='Events Scheduler', string=kiv, app_data=True, main_color='Orange', pre_string=pre, toolbar=True,
        list_of_dirs=["Tasks"]).run()
