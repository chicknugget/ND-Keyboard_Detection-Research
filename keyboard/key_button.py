from kivy.uix.button import Button
from kivy.clock import Clock
import time
from data.models import KeystrokeEvent

class KeyButton(Button):
    """A single keyboard key that captures touch events with precise timing"""
    
    def __init__(self, key_char, key_id, on_key_press=None,**kwargs):
        super().__init__(**kwargs)
        self.key_char = key_char
        self.key_id = key_id
        self.text = key_char
        self.on_key_press = on_key_press
        self.active_touch = None
        self.press_time = None

    def on_touch_down(self, touch): #touch: event object from kivy containing position of touch
        """Called when finger touches the screen"""
        if self.collide_point(*touch.pos): #kivy method:checks if position inside boundaries
            self.active_touch = touch
            self.press_time = time.perf_counter_ns()
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """Called when finger lifts from the screen"""
        if touch == self.active_touch: #self.active_touch: touch we stored in touch down
            release_time = time.perf_counter_ns() #func to return current time in nanosecs
            hold_duration_ns = release_time - self.press_time

            #creating a keystroke event
            keystroke = KeystrokeEvent(
                session_id="",  # Will be set by parent
                task_type="",   # Will be set by parent
                key_id=self.key_id,
                key_char=self.key_char,
                press_time_ms=self.press_time // 1_000_000,
                release_time_ms=release_time // 1_000_000,
                hold_duration_ms=hold_duration_ns // 1_000_000,
                inter_key_interval_ms=None,  # Parent calculates this
                flight_time_ms=None,         # Parent calculates this
                touch_x=touch.pos[0],
                touch_y=touch.pos[1],
                key_center_x=self.center_x,
                key_center_y=self.center_y
            )

            #sending to parent via callback
            if self.on_key_press:
                self.on_key_press(keystroke)
            
            self.active_touch = None
            return True
        return super().on_touch_up(touch)