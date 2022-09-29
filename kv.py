

pre = """
<loop>
    orientation: "vertical"
    size_hint_y: None
    height: "70dp"

    MDTextField:
        id: i_
        text: app.iterations
        hint_text: "Choose the number of iteration for this task"
        size_hint_x: 0.25
        input_filter: "int"
        font_size: 24
        on_text_validate: app.add("i")


<rename>
    orientation: "vertical"
    size_hint_y: None
    height: "70dp"

    MDTextField:
        id: rename_
        hint_text: "Enter a new name"
        size_hint_x: 0.9
        font_size: 24
        on_text_validate: app.add("rename-box")

<cmd>
    orientation: "vertical"
    size_hint_y: None
    height: "70dp"

    MDIconButton:
        icon: "information"
        pos_hint: {"center_x": 0.9}
        user_font_size: "32sp"
        on_press: app.url()



    MDTextField:
        id: cmd_
        hint_text: "Enter a cmd command"
        size_hint_x: 0.9
        font_size: 24
        on_text_validate: app.add("console")


<iter>
    orientation: "vertical"
    size_hint_y: None
    height: "80dp"

    MDTextField:
        id: iter_
        hint_text: "Choose the number of iteration for this script"
        size_hint_x: 0.4
        input_filter: "int"
        font_size: 24

<ItemConfirm>
    on_press: root.set_icon(check)

    CheckboxLeftWidget:
        id: check
        group: "check"

<size>
    orientation: "vertical"
    size_hint_y: None
    height: "140dp"

    MDTextField:
        id: state_
        hint_text: "Maximize / Normal / Minimize"
        size_hint_x: 0.4
        font_size: 24
        on_text_validate: app.add("overscan")

    MDTextField:
        id: window_
        hint_text: "Specify window name (not required)"
        size_hint_x: 0.4
        font_size: 24  
        on_text_validate: app.add("overscan")

<Load>
    orientation: "vertical"
    size_hint_y: None
    height: "100dp"

    BoxLayout:
        orientation: 'vertical'
        ScrollView:
            size_hint_y: None
            BoxLayout:
                id: YourTaskName
                orientation: 'horizontal'
                size_hint_x: None
                width: self.minimum_width
        AutoCompleter:
            size_hint_y: None
            container: YourTaskName
            size_hint_x: 0.6
            color_mode: 'accent'
            font_size: 24
        Widget:

<index>
    orientation: "vertical"
    size_hint_y: None
    height: "80dp"

    MDTextField:
        id: moveto
        hint_text: "Choose a position"
        size_hint_x: 0.4
        font_size: 24

<random>
    orientation: "vertical"
    size_hint_y: None
    height: "130dp"

    MDTextField:
        id: options_
        hint_text: "Letters and symbols options"
        helper_text: "Example: ab123%^>dv"
        helper_text_mode: "on_focus"
        size_hint_x: 0.9
        font_size: 24

    MDTextField:
        id: length_
        hint_text: "Phrase length"
        helper_text: "Example: 3-7 or just one number"
        helper_text_mode: "on_focus"
        size_hint_x: 0.5
        font_size: 24

<fixed>
    orientation: "vertical"
    size_hint_y: None
    height: "120dp"

    MDTextField:
        id: key_
        hint_text: "Write a phrase"
        size_hint_x: 0.4
        font_size: 24
        multiline: True
        on_text_validate: app.add("keyboard")

<Save>
    orientation: "vertical"
    size_hint_y: None
    height: "80dp"

    MDTextField:
        id: kl
        hint_text: "Task name"
        size_hint_x: 0.4
        font_size: 24
        on_text_validate: app.add("content-save")


<ContentMouseMove>
    orientation: "vertical"
    size_hint_y: None
    height: "190dp"

    MDTextField:
        id: x_
        hint_text: "X position"
        size_hint_x: 0.4
        font_size: 24
        on_text_validate: app.add("mouse-move-vertical")

    MDTextField:
        id: y_
        hint_text: "Y position"
        size_hint_x: 0.4
        font_size: 24
        on_text_validate: app.add("mouse-move-vertical")

    MDTextField:
        text: "0"
        id: duration_
        size_hint_x: 0.4
        helper_text: "Duration"
        font_size: 20
        helper_text_mode: "persistent"
        on_text_validate: app.add("mouse-move-vertical")

<Content>
    orientation: "vertical"
    size_hint_y: None
    height: "60dp"

    MDTextField:
        id: time_
        hint_text: "Time to wait"
        size_hint_x: 0.4
        font_size: 24
        on_text_validate: app.add("clock-time-three")


<ContentClick>
    orientation: "vertical"
    size_hint_y: None
    height: "50dp"

    MDSwitch:
        id: click_
        width: 50
        active: False 

<ContentNavigationDrawer>:
    ScrollView:
        MDList:
            TwoLineIconListItem:
                text: "Home"
                secondary_text: "Your main screen"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "Home"
                IconLeftWidget:
                    icon: "home"

            TwoLineIconListItem:
                text: "Settings"
                secondary_text: "Your settings screen"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "Settings"
                    app.task_manager()
                IconLeftWidget:
                    icon: "cog"
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
        data: app.list  
        bg_hint_color: app.theme_cls.primary_light
        callback: app.callback
"""
