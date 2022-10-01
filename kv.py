

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
    height: "70dp"
    spacing: "10dp"

    MDTextField:
        id: python_command_input
        hint_text: "Enter a python command"
        size_hint_x: 0.9
        font_size: "20dp"
        
<WebsitePopup>
    orientation: "vertical"
    size_hint_y: None
    height: "70dp"
    spacing: "10dp"

    MDTextField:
        id: url_input
        hint_text: "Enter the website url"
        size_hint_x: 0.9
        font_size: "20dp"

<SendEmail>
    orientation: "vertical"
    size_hint_y: None
    height: "250dp"
    spacing: "10dp"
    
    Input:
        id: email_to_input
        hint_text: "Enter email address"
        size_hint_x: 1
    
    Input:
        id: email_subject_input
        hint_text: "Enter a subject"
        size_hint_x: 1
        font_size: "16dp"
        
    Input:
        id: email_message_input
        hint_text: "Enter a message"
        size_hint_x: 1
        font_size: "16dp"
        multiline: True
        size_hint_y: "100dp"
        
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
            text_color: 1, 1, 1, 1
            icon_color: 1, 1, 1, 1
            on_release: app.current_task_config.pick_start_date()
        
        BtnIcon:
            id: start_time
            icon: "clock-time-four"
            text: "  Start Time"
            size_hint_x: 1
            text_color: 1, 1, 1, 1
            icon_color: 1, 1, 1, 1
            on_release: app.current_task_config.pick_start_time()
                        
        
    Text:
        text: "Run every 40 minutes and 30 seconds"
    
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
            
<EditTask>
    orientation: "vertical"
    size_hint_y: None
    height: "80dp"
    
    Text:
        text: "Are you sure you want to delete this task?\\nThis action cannot be undone."
        font_size: "18dp"
        bold: True

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
