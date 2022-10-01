import os
from kivy.uix.boxlayout import BoxLayout
from actions.base_task import BaseTask


class SystemCommand(BaseTask):
    action = "System Command"

    def config(self, gui):
        cmd_popup = type("SystemCommand", (BoxLayout,), {})()

        def okay_func(*args):
            cmd = cmd_popup.ids.cmd_command_input.text
            if not cmd:
                gui.toast("Please enter a command", 5)
                return
            gui.open_task_config(self.action, {"command": cmd})

        gui.popup_kivy4(title="Run System Command", content=cmd_popup, okay_func=okay_func)

    def run(self, content: dict[str, str]):
        os.system(content["command"])
