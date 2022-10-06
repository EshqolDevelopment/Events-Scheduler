import time

import macro_creator
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy4 import thread
from actions.base_task import BaseTask


class MacroRecorder(BaseTask):
    action = "Macro Recorder"

    def __init__(self):
        self.macro = macro_creator.Recorder(stop_key="esc")
        self.macro_popup = None

    def config(self, gui):
        gui.record_macro = self.record_macro
        self.macro_popup = type("MacroRecorderDialog", (BoxLayout,), {})()
        gui.popup_kivy4(title="Keyboard and mouse recorder", content=self.macro_popup, okay_func=lambda *args: gui.open_task_config(self.action, self.macro.recorded), okay_text="Continue", cancel_text="Cancel", auto_dismiss=False)

    @thread
    def record_macro(self):
        self.update_btn321()
        self.macro.record()
        self.update_macro_btn("Macro Saved")

    @mainthread
    def update_macro_btn(self, text: str):
        macro_btn = self.macro_popup.ids.recording_btn
        macro_btn.text = text

    def update_btn321(self):
        for i in range(3):
            self.update_macro_btn(str(3 - i))
            time.sleep(1)
        self.update_macro_btn("Recording...")

    def run(self, content: dict[str, str]):
        self.macro.recorded = content
        self.macro.play()
