from datetime import datetime
from typing import TYPE_CHECKING
from kivy.uix.boxlayout import BoxLayout
from task import Task
from time_operations import reformat_date, reformat_time

if TYPE_CHECKING:
    from main import App


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

    def pick_start_date(self):
        self.gui.show_date_picker(on_save=lambda *args: self.save_start_date(args[1]))

    def save_start_date(self, chosen_date: datetime.date):
        self.start_date = reformat_date(chosen_date)
        self.save_popup.ids.start_date.text = f"  Start Date: {self.start_date}"

    def pick_start_time(self):
        self.gui.show_time_picker(on_save=lambda *args: self.save_start_time(args[1]))

    def save_start_time(self, chosen_time: datetime.time):
        self.start_time = reformat_time(chosen_time)
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
