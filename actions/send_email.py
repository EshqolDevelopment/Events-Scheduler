from kivy.uix.boxlayout import BoxLayout
from actions.base_task import BaseTask


class SendEmail(BaseTask):
    action = "Send Email"

    def config(self, gui):
        email_popup = type("SendEmail", (BoxLayout,), {})()
        gui.popup_kivy4(title="Send Email", content=email_popup,
                        okay_func=lambda *args: gui.open_task_config(
                            self.action,
                            {"to": email_popup.ids.email_to_input.text,
                             "subject": email_popup.ids.email_subject_input.text,
                             "message": email_popup.ids.email_message_input.text}))

    def run(self, content: dict[str, str]):
        print("Sending email to", content["to"])
