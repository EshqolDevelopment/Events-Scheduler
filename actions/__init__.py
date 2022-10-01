from actions.open_app import OpenApp
from actions.open_website import OpenWebsite
from actions.python_command import PythonCommand
from actions.send_email import SendEmail
from actions.system_command import SystemCommand

action_dict = {
    'Open App': {
        "icon": 'launch',
        "class": OpenApp()
    },
    'System Command': {
        "icon": 'console',
        "class": SystemCommand()
    },
    'Send Email': {
        "icon": 'email',
        "class": SendEmail()
    },
    'Python Command': {
        "icon": 'language-python',
        "class": PythonCommand()
    },
    'Open Website': {
        "icon": 'web',
        "class": OpenWebsite()
    },
}
