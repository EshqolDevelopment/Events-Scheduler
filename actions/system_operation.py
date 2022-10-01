from kivy.uix.boxlayout import BoxLayout
from actions.base_task import BaseTask
import os


class SystemOperation(BaseTask):
    action = "System Operation"

    def config(self, gui):
        system_operation_popup = type("SystemOperation", (BoxLayout,), {})()

        gui.popup_kivy4(title="System Operation",
                        content=system_operation_popup,
                        okay_func=lambda *args: gui.toast("Choose an operation", 5))

    def run(self, content: dict[str, str]):
        os.system(content["command"])
