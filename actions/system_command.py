import os
from kivy.uix.boxlayout import BoxLayout
from actions.base_task import BaseTask


class SystemCommand(BaseTask):
    action = "System Command"

    def config(self, gui):
        cmd_popup = type("SystemCommand", (BoxLayout,), {})()
        gui.popup_kivy4(title="Run System Command", content=cmd_popup,
                        okay_func=lambda *args: gui.open_task_config(
                            self.action,
                            {"command": cmd_popup.ids.cmd_command_input.text}))

    def run(self, content: dict[str, str]):
        os.system(content["command"])
