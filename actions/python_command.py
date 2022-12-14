from kivy.uix.boxlayout import BoxLayout
from actions.base_task import BaseTask


class PythonCommand(BaseTask):
    action = "Python Command"

    def config(self, gui):
        python_popup = type("PythonCommand", (BoxLayout,), {})()

        def okay_func(*args):
            python_command = python_popup.ids.python_command_input.text
            if not python_command:
                gui.toast("Please enter a Python command", 5)
                return
            gui.open_task_config(self.action, {"command": python_command})

        gui.popup_kivy4(title="Run Python Command", content=python_popup, okay_func=okay_func)

    def run(self, content: dict[str, str]):
        exec(content["command"])
