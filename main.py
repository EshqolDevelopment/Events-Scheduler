from kivymd.uix.list import ThreeLineAvatarIconListItem, IconLeftWidget, OneLineAvatarIconListItem
import webbrowser
from kivy4 import *
from kv import *


action_list = {
    'Open App': 'launch',
    'System Command': 'console',
    'Send Email': 'email',
    'Python Command': 'language-python',
    'Open Website': 'web',
}

class Action:

    def __init__(self, name: str, action: str, unix: float, params: dict):
        self.name = name
        self.action = action
        self.unix = unix
        self.params = params

    def wait_for_time(self):
        while True:
            if time.time() >= self.unix:
                break

            if time.time() >= self.unix - 60:
                print("60 seconds left")
                time.sleep(1)

            time.sleep(time.time() - self.unix - 60)

    def execute(self):
        self.wait_for_time()

        if self.action == 'launch':
            os.startfile(self.params['app'])

        elif self.action == 'console':
            os.system(self.params['command'])

        elif self.action == 'email':
            pass

        elif self.action == 'language-python':
            exec(self.params['command'])

        elif self.action == 'web':
            webbrowser.open(self.params['url'])




class App(Kivy4):

    list = action_list

    def on_start(self):

        item = ThreeLineAvatarIconListItem(text="Here you can create and edit tasks",
                                           secondary_text="Press on the + to add step and save your task with the save icon",
                                           tertiary_text="Edit your existing task with the pen file icon at the top bar")

        item.add_widget(
            IconLeftWidget(icon="repeat", on_press=lambda p: self.dialog("loop()", "repeat", index=True)))

        self.ids.container.add_widget(item)

        task = OneLineAvatarIconListItem(text="Task 1", on_press=lambda p: self.dialog("loop()", "repeat", index=True))
        self.ids.container.add_widget(task)

    def add_row(self, name: str):
        data = self.getFile(f"tasks/{name}", extension=".schedule", is_json=True)

        unix = data['unix']
        action = data['action']
        params = data['params']

        action = Action(name, action, unix, params)
        action.execute()






    def get_key(self, *args):
        return "hello"

    def callback(self, x):
        icon = x.icon
        print(icon)

    def get_icon(self):
        return self.moon_icon


if __name__ == '__main__':
    App(app_name='Events Scheduler', string=kiv, app_data=True, main_color='Orange', pre_string=pre,
        toolbar=['[[app.dark_mode_icon, lambda x: app.reverseDarkMode()]]',
                 '[]']).run()
