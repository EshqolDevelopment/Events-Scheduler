import webbrowser

from kivy.uix.boxlayout import BoxLayout
from actions.base_task import BaseTask


class OpenWebsite(BaseTask):
    action = "Open Website"

    def config(self, gui):
        website_popup = type("OpenWebsite", (BoxLayout,), {})()
        gui.popup_kivy4(title="Open Website", content=website_popup,
                        okay_func=lambda *args: gui.open_task_config(
                            self.action,
                            {"website": website_popup.ids.website_input.text}))

    def run(self, content: dict[str, str]):
        webbrowser.open(content["url"])
