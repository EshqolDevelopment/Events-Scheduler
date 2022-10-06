from actions.open_app import OpenApp
from actions.open_website import OpenWebsite
from actions.python_command import PythonCommand
from actions.system_operation import SystemOperation
from actions.system_command import SystemCommand
from actions.macro_recorder import MacroRecorder

action_dict = {
    'Open App': {
        "icon": 'launch',
        "class": OpenApp()
    },
    'System Command': {
        "icon": 'console',
        "class": SystemCommand()
    },
    'System Operation': {
        "icon": 'microsoft-windows',
        "class": SystemOperation()
    },
    'Python Command': {
        "icon": 'language-python',
        "class": PythonCommand()
    },
    'Open Website': {
        "icon": 'web',
        "class": OpenWebsite()
    },
    'Macro Recorder': {
        "icon": "radiobox-marked",
        "class": MacroRecorder()
    }
}
