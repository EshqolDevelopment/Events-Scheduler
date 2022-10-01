import webbrowser

from kivy.uix.boxlayout import BoxLayout
from actions.base_task import BaseTask


class OpenWebsite(BaseTask):
    action = "Open Website"

    def config(self, gui):
        website_popup = type("OpenWebsite", (BoxLayout,), {})()

        def okay_func(*args):
            url = website_popup.ids.url_input.text
            if not url:
                gui.toast("Please enter a URL", 5)
                return
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url
            gui.open_task_config(self.action, {"website": url})

        gui.popup_kivy4(title="Open Website", content=website_popup, okay_func=okay_func)

    def run(self, content: dict[str, str]):
        webbrowser.open(content["url"])
