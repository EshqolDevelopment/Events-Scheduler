

pre = """
<SystemCommand>
    orientation: "vertical"
    size_hint_y: None
    height: "70dp"
    spacing: "10dp"

    MDTextField:
        id: cmd_command_input
        hint_text: "Enter a cmd command"
        size_hint_x: 0.9
        font_size: "20dp"
       
        
<PythonCommand>
    orientation: "vertical"
    size_hint_y: None
    height: "140dp"
    spacing: "10dp"

    Input:
        id: python_command_input
        hint_text: "Enter python code"
        multiline: True
        size_hint_x: 1
        font_size: "18dp"
        size_hint_y: 0.9
        
        
<OpenWebsite>
    orientation: "vertical"
    size_hint_y: None
    height: "70dp"
    spacing: "10dp"

    MDTextField:
        id: url_input
        hint_text: "Enter the website url"
        size_hint_x: 0.9
        font_size: "20dp"

<SystemOperation>
    orientation: "vertical"
    size_hint_y: None
    height: "300dp"
    spacing: "10dp"
        
    MDList:
        id: system_operation_list
        selected_mode: True
        OneLineListItem:
            text: "Shutdown"
            on_release: app.open_task_config("System Operation", {"command": "shutdown /s /t 0"})
        OneLineListItem:
            text: "Restart"
            on_release: app.open_task_config("System Operation", {"command": "shutdown /r /t 0"})
        OneLineListItem:
            text: "Log off"
            on_release: app.open_task_config("System Operation", {"command": "shutdown /l"})
        OneLineListItem:
            text: "Lock"
            on_release: app.open_task_config("System Operation", {"command": "rundll32.exe user32.dll,LockWorkStation"})
        OneLineListItem:
            text: "Sleep"
            on_release: app.open_task_config("System Operation", {"command": "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"})
        OneLineListItem:
            text: "Hibernate"
            on_release: app.open_task_config("System Operation", {"command": "rundll32.exe powrprof.dll,SetSuspendState 1,1,0"}) 
     
        
<SavePopup>
    orientation: "vertical"
    size_hint_y: None
    height: "240dp"
    spacing: "30dp"
    
    MDTextField:
        id: save_name_input
        hint_text: "Enter a name for your task"
        size_hint_x: 1
        font_size: "22dp"
        mode: "rectangle"
            
    BoxLayout:
        spacing: "20dp"
        orientation: "horizontal"
        BtnIcon:
            id: start_date
            icon: "calendar-range"
            text: "  Start Date"
            size_hint_x: 1
            on_release: app.current_task_config.pick_start_date()
        
        BtnIcon:
            id: start_time
            icon: "clock-time-four"
            text: "  Start Time"
            size_hint_x: 1
            on_release: app.current_task_config.pick_start_time()
                        
        
    Text:
        text: app.parse_repeat_text(days_input.text, hours_input.text, minutes_input.text) 
        id: repeat_text
    
    BoxLayout:
        spacing: "5dp"
        
        Input:
            id: days_input
            hint_text: "Days"
        
        Input:
            id: hours_input
            hint_text: "Hours"
        
        Input:
            id: minutes_input
            hint_text: "Minutes"     
            
<DeleteTask>
    orientation: "vertical"
    size_hint_y: None
    height: "80dp"
    
    Text:
        text: "Are you sure you want to delete this task?\\nThis action cannot be undone."
        font_size: "18dp"
        bold: True
        
<Welcome>
    orientation: "vertical"
    size_hint_y: None
    height: "340dp"
    
    Text:
        text: "Welcome to Task Scheduler!\\n\\nTo get started, click the plus button in the bottom right corner to add a task.\\n\\nTou can change the theme from dark to light in the top right corner.\\n\\nTask Schedular pro is design to replace the default windows alternative, with a modern and simpler interface.\\n\\nThe app allow anyone without any technical knowledge to use it.\\n\\nHere is the list of the supported tasks:\\n  - System Command\\n  - Python Command\\n  - Open Website\\n  - System Operation"
        halign: "left"

"""


kiv = """   
Screen:
    name: "Home"  
    BoxLayout:
        orientation: "vertical"
        spacing: "10dp"
        id: mdcard
        pos_hint: {"center_x": 0.5, "center_y": 0.425}
        padding: 15
        MDScrollView:
            id: refresh_layout
            root_layout: root
            MDList:
                id: container

    MDFloatingActionButtonSpeedDial:
        data: app.action_to_icon  
        bg_hint_color: app.theme_cls.primary_light
        callback: app.callback
        
"""
