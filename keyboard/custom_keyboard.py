from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from keyboard.key_button import KeyButton
from data.models import KeystrokeEvent

class CustomKeyboard(BoxLayout):
    """Full QWERTY keyboard capturing keystroke timing data"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.session_id = None
        self.task_type = None
        self.previous_keystroke = None
        self.shift_active = True
        self.on_keystroke_callback = None

        self.build_keyboard()

    def build_keyboard(self):
        """to create keyboard layout"""
        row1_keys = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
        row2_keys = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']
        row3_keys = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']

        #creating first two row of only letters
        row1 = self.create_key_row(row1_keys)
        row2 = self.create_key_row(row2_keys)

        #creating third row of shift, letters, backspace
        row3 = self.create_row3_with_special_keys(row3_keys)

        #comma, spacebar, fullstop
        row4 = GridLayout(cols=4, size_hint_y=0.25, spacing=2)
        
        comma_key = KeyButton(key_char=",", key_id="key_comma", on_key_press=self.handle_keystroke)
        space_key = KeyButton(key_char=" ", key_id="key_space", on_key_press=self.handle_keystroke, text="SPACE")
        period_key = KeyButton(key_char=".", key_id="key_period", on_key_press=self.handle_keystroke)
        done_key = KeyButton(key_char="✓", key_id="key_done", on_key_press=self.handle_keystroke, text="DONE")

        row4.add_widget(comma_key)
        row4.add_widget(space_key)
        row4.add_widget(period_key)
        row4.add_widget(done_key)
        
        #adding all 4th row special key to keyboard
        self.add_widget(row1)
        self.add_widget(row2)
        self.add_widget(row3)
        self.add_widget(row4)

    def create_key_row(self, keys, **kwargs):
        """Create a row of keyboard keys"""
        row = GridLayout(cols=len(keys), size_hint_y=0.25, spacing=2)

        for key_char in keys:
            key = KeyButton(
                key_char=key_char,
                key_id=f"key_{key_char.lower()}",
                on_key_press=self.handle_keystroke
            )
            row.add_widget(key)

        return row  

    def create_row3_with_special_keys(self, keys):
        """Create row 3 with SHIFT and BACKSPACE"""
        row = GridLayout(cols=len(keys) + 2, size_hint_y=0.25, spacing=2)
        
        # Add SHIFT button
        shift_key = KeyButton(
            key_char="SHIFT",
            key_id="key_shift",
            on_key_press=self.handle_keystroke
        )
        row.add_widget(shift_key)
        
        # Add letter keys
        for key_char in keys:
            key = KeyButton(
                key_char=key_char,
                key_id=f"key_{key_char.lower()}",
                on_key_press=self.handle_keystroke
            )
            row.add_widget(key)
        
        # Add BACKSPACE button
        backspace_key = KeyButton(
            key_char="BCK",
            key_id="key_backspace",
            on_key_press=self.handle_keystroke
        )
        row.add_widget(backspace_key)
        
        return row

    def handle_keystroke(self, keystroke):
        """Process keystroke from KeyButton - add context and calculate intervals"""
        keystroke.session_id = self.session_id
        keystroke.task_type = self.task_type

        if self.previous_keystroke:
            keystroke.inter_key_interval_ms = (keystroke.press_time_ms - self.previous_keystroke.release_time_ms)
            keystroke.flight_time_ms = keystroke.press_time_ms - self.previous_keystroke.press_time_ms

        if keystroke.key_char == 'SHIFT':
            self.shift_active = not self.shift_active
            return 
        if self.shift_active:
            keystroke.key_char = keystroke.key_char.upper()
        else:
            keystroke.key_char = keystroke.key_char.lower()
        if self.shift_active and keystroke.key_char not in [' ', ',', '.']:
            self.shift_active = False
        if keystroke.key_char == '.':
            self.shift_active = True

        self.previous_keystroke = keystroke

        # For testing - print keystroke data
        print(f"Key: {keystroke.key_char} | Hold: {keystroke.hold_duration_ms}ms | "
              f"Interval: {keystroke.inter_key_interval_ms}ms | Task: {keystroke.task_type}")

        if self.on_keystroke_callback:
            self.on_keystroke_callback(keystroke)      

    def set_session(self, session_id):
        """setting the current session ID: from person A"""
        self.session_id = session_id
    
    def set_task(self, task_type):
        """setting the current task type and reset for new sentence: from person B"""
        self.task_type = task_type
        self.previous_keystroke = None

    def reset(self):
        """Reset keyboard state for new sentence"""
        self.previous_keystroke = None
        self.shift_active = False
    
    def set_on_keystroke_callback(self, callback):
        """Set callback function for keystroke events"""
        self.on_keystroke_callback = callback #***
