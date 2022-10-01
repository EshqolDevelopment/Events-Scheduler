from kivy.uix.boxlayout import BoxLayout
from actions.base_task import BaseTask


class PythonCommand(BaseTask):
    action = "Python Command"

    def config(self, gui):
        python_popup = type("PythonCommand", (BoxLayout,), {})()
        gui.popup_kivy4(title="Run Python Command", content=python_popup,
                        okay_func=lambda *args: gui.open_task_config(
                            self.action, {"command": python_popup.ids.python_command_input.text}))

    def run(self, content: dict[str, str]):
        exec(content["command"])
