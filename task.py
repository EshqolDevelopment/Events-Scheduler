import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from actions import action_dict
from kivy4 import thread
from typing import TYPE_CHECKING
from time_operations import reformat_extend_date
import hashlib
if TYPE_CHECKING:
    from main import App


@dataclass
class Task:
    name: str
    action: str
    content: dict[str, str]
    start_date: str
    start_time: str
    repeat_every: dict[str, int]
    next_run_time: str | None

    @property
    def id(self):
        sha1 = hashlib.sha1()
        sha1.update(self.name.encode())
        return sha1.hexdigest()

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
                while next_run_time <= datetime.now():
                    next_run_time += timedelta(**self.repeat_every)

                self.next_run_time = reformat_extend_date(next_run_time)
                gui.set_file(f"Tasks/{self.id}", self.__dict__, is_json=True)
                gui.update_task_row(self)

            time.sleep(1)

    def run_task(self):
        action = self.action
        content = self.content
        action_dict[action]["class"].run(content)

    def stop(self):
        self.next_run_time = "Stop"
