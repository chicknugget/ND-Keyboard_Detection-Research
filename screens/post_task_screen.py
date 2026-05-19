# screens/post_task_screen.py 

import os

from keyboard.custom_keyboard import CustomKeyboard
from data.models import KeystrokeEvent, EmotionLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings, PixelUI, BASE_PATH
from screens.pixel_ui_wrapper import PixelFrame

MIN_TYPING_LENGTH = 16
 
SENTENCE_OPTIONS = [
    'This Game is Relaxing.',
    'This Game makes me Happy.',
    'This Game makes me Sad.',
    'This Game is Frustrating.',
    'This Game makes me Stressed.',
    'This Game is Boring.'
]

class EmojiImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = True

class PostTaskScreen(BaseScreen):
    task_type = StringProperty('relaxation')
    selected_emoji = StringProperty('')
    typed_length = NumericProperty(0)
    
    def __init__(self, task_type='relaxation', **kwargs):
        super(PostTaskScreen, self).__init__(**kwargs)
        self.task_type = task_type
        
        # Create pixel frame wrapper with title
        self.pixel_frame = PixelFrame(
            title='FEEDBACK',
            show_stars=False,
            show_header=True,
            show_quit=False,
            show_reset=False
        )
        
        # Main vertical layout (preserved structure)
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(6), dp(4), dp(6), dp(4)],
            spacing=dp(6)
        )
        
        # Sentences instruction card 
        sentences_card = self.create_card(
            size_hint=(1, None), 
            height=dp(140),
            padding=dp(6)
        )
        
        sentences_text = '\n'.join([f"{i+1}. {s}" for i, s in enumerate(SENTENCE_OPTIONS)])
        sentences_label = Label(
            text=sentences_text,
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.PIXEL_BODY_SMALL,
            color=Colors.TEXT_BLACK,
            halign='left',
            valign='top',
            text_size=(None, None)
        )
        sentences_label.bind(size=sentences_label.setter('text_size'))
        sentences_card.add_widget(sentences_label)
        main_layout.add_widget(sentences_card)
        
        # Input box
        self.typed_display = self.create_input_field(
            hint_text='Tap here & type any one sentence here...',
            multiline=True
        )
        self.typed_display.font_name = PixelUI.FONT_BODY
        # Block the OS keyboard — input comes from CustomKeyboard
        # is_focusable is kept True so tapping shows a cursor and triggers focus
        self.typed_display.keyboard_mode = 'managed'
        self.typed_display.is_focusable = True
        # self.typed_display.is_focusable = False
        self.typed_display.bind(text=self.on_text_change)
        self.typed_display.bind(focus=self.on_text_focus)
        main_layout.add_widget(self.typed_display)
        
        # Character counter
        self.char_counter = Label(
            text=f'0 / {MIN_TYPING_LENGTH} characters (minimum)',
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.BODY_TINY,
            color=Colors.DISABLED_GRAY,
            size_hint_y=None,
            height=dp(16),
            halign='right'
            # width will auto-adjust based on text
        )
        main_layout.add_widget(self.char_counter)
        
        #Emoji selection title
        self.emoji_title = Label(
            text='Select your feeling:',
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.PIXEL_BODY_SMALL,
            color=Colors.WARNING_ORANGE ,
            size_hint_y=None,
            height=dp(20),
            opacity=0
        )
        main_layout.add_widget(self.emoji_title)
        
        # Emoji grid
        self.emoji_grid = GridLayout(
            cols=6,
            size_hint_y=None,
            height=dp(60),
            spacing=dp(4),
            padding=dp(2)
        )
        self.emoji_buttons = []
        
        for emoji in Strings.FIXED_EMOJIS:
            btn = EmojiImageButton(
                source= os.path.join(BASE_PATH,emoji['source']),
                size_hint=(None, None),
                size=(dp(45), dp(45)),
                opacity=0.5
            )
            btn.emoji_id = emoji['id']
            btn.bind(on_press=lambda x, e=emoji['id']: self.select_emoji(e))
            self.emoji_grid.add_widget(btn)
            self.emoji_buttons.append(btn)

        # Emoji row background card
        self.emoji_card = self.create_card(
            size_hint=(1, None),
            height=dp(72),
            padding=dp(4),
            bg_color=Colors.BACKGROUND_LIGHT_GRAY
        )
        self.emoji_card.opacity = 0
        self.emoji_card.add_widget(self.emoji_grid)
        main_layout.add_widget(self.emoji_card)
        
        #  KEYBOARD PLACEHOLDER
        self.keyboard_placeholder = self.create_card(
            size_hint=(1, None),
            height=0,  # Hidden initially
            padding=dp(1)
        )
        self.keyboard_placeholder.opacity = 0
        
        # Create larger keyboard - increased height
        self.keyboard = CustomKeyboard()
        self.keyboard_placeholder.add_widget(self.keyboard)

        main_layout.add_widget(self.keyboard_placeholder)

        
        # Submit button container
        submit_container = BoxLayout(
            size_hint_y=None,
            height=dp(56),
            padding=(dp(2), 0)
        )
        self.submit_btn = self.create_button(
            text=Strings.BTN_SUBMIT,
            on_press=self.on_submit,
            button_type='success',
            disabled=True
        )
        submit_container.add_widget(self.submit_btn)
        main_layout.add_widget(submit_container)
        
        # Set content to pixel frame
        self.pixel_frame.set_content(main_layout)
        self.add_widget(self.pixel_frame)
    
    def on_enter(self):
        """Reset for fresh task"""
        super().on_enter()
        self.reset_screen()
        self.typed_display.disabled = False
        self.typed_display.readonly = False
        Clock.schedule_once(lambda *_: setattr(self.typed_display, 'focus', False), 0)

        app = App.get_running_app()
        self.keyboard.set_session(app.user_data['session_id'])
        self.keyboard.set_task(self.task_type)
        self.keyboard.set_on_keystroke_callback(self.on_keystroke)
        self.keyboard.reset()
    
    def reset_screen(self):
        self.typed_display.text = ''
        self.typed_display.focus = False
        self.typed_display.disabled = False
        self.typed_display.readonly = False
        self.typed_length = 0
        self.selected_emoji = ''
        self.char_counter.text = f'0 / {MIN_TYPING_LENGTH} characters (minimum)'
        self.char_counter.color = Colors.TEXT_GRAY
        self.emoji_title.opacity = 0
        self.emoji_grid.opacity = 0
        self.emoji_card.opacity = 0
        for btn in self.emoji_buttons:
            btn.opacity = 0
            btn.disabled = True
        self.submit_btn.disabled = True
        self.submit_btn.background_color = Colors.DISABLED_GRAY
        self.emoji_click_history = []   # track every emoji tap
        self.keystroke_count = 0
        self.backspace_count = 0
        # Hide the keyboard on reset
        self.keyboard_placeholder.height = 0
        self.keyboard_placeholder.opacity = 0
        # Show title when keyboard is hidden
        self.pixel_frame.show_title()
        print(f"PostTaskScreen({self.task_type}) reset")

    def on_text_focus(self, instance, focused):
        """Show custom keyboard when text box is tapped; hide when focus is lost."""
        if focused:
            # Enlarged keyboard height
            self.keyboard_placeholder.height = dp(188)
            self.typing_start_time = int(__import__('__time__').time() * 1000)
            self.keyboard_placeholder.opacity = 1
        else:
            self.keyboard_placeholder.height = 0
            self.keyboard_placeholder.opacity = 0
    
    def on_text_change(self, instance, value):
        self.typed_length = len(value)
        self.char_counter.text = f'{self.typed_length} / {MIN_TYPING_LENGTH} characters (minimum)'
        
        if self.typed_length >= MIN_TYPING_LENGTH:
            #  ENABLE EMOJIS
            self.char_counter.color = Colors.SUCCESS_GREEN
            self.emoji_title.opacity = 1
            self.emoji_grid.opacity = 1
            self.emoji_card.opacity = 1
            for btn in self.emoji_buttons:
                btn.opacity = 0.8
                btn.disabled = False
        else:
            #  DISABLE EMOJIS
            self.char_counter.color = Colors.WARNING_ORANGE
            self.emoji_title.opacity = 0.1
            self.emoji_grid.opacity = 0.1
            self.emoji_card.opacity = 0.1
            for btn in self.emoji_buttons:
                btn.opacity = 0.1
                btn.disabled = True
            self.selected_emoji = ''
            self.submit_btn.disabled = True
            self.submit_btn.background_color = Colors.DISABLED_GRAY
    
    def select_emoji(self, emoji_id):
        self.selected_emoji = emoji_id
        self.emoji_click_history.append(emoji_id)   # record every tap
        # Reset all to muted
        for btn in self.emoji_buttons:
            btn.opacity = 0.8
        # Highlight selected
        for btn in self.emoji_buttons:
            if btn.emoji_id == emoji_id:
                btn.opacity = 1.0
                break
        # Enable submit
        self.submit_btn.disabled = False
        self.submit_btn.background_color = Colors.SUCCESS_GREEN
    
    def add_char(self, char):
        """Keyboard input handler - Person C uses this"""
        self.typed_display.text += char
        # Trigger text change to update emoji state
        self.on_text_change(self.typed_display, self.typed_display.text)

    def backspace(self, instance):
        """Backspace handler - Person C uses this"""
        self.typed_display.text = self.typed_display.text[:-1]
        # Trigger text change to update emoji state
        self.on_text_change(self.typed_display, self.typed_display.text)


    def on_submit(self, instance):
        from datetime import datetime
        
        app = App.get_running_app()
        if self.typed_length < MIN_TYPING_LENGTH or not self.selected_emoji:
            print(" Invalid submission")
            return
        self.typed_display.focus = False
        
        # Get current timestamp for this task
        task_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Build complete task data for backend submission
        task_data = {
            # Identifiers
            'participant_id': app.user_data.get('participant_id', ''),
            'session_id': app.user_data.get('session_id', ''),
            
            # Session timing
            'session_start_time': app.user_data.get('session_start_time', ''),
            
            # Task details
            'task_number': app.user_data.get('current_game', 0),
            'task_type': self.task_type,
            'typed_text': self.typed_display.text.strip(),
            'selected_emoji': self.selected_emoji,           # final choice
            'emoji_click_history': list(self.emoji_click_history),  # all taps in order
            
            # Additional metadata
            'text_length': self.typed_length,
            'task_timestamp': task_timestamp
        }
        
        # Append to tasks list
        app.user_data.setdefault('tasks', []).append(task_data)
        typing_duration = int(import('time').time() * 1000) - getattr(self, 'typing_start_time', 0)
        emotion_label = EmotionLabel(
            session_id=app.user_data.get('session_id', ''),
            task_type=self.task_type,
            selected_emoji=self.selected_emoji,
            typed_sentence=self.typed_display.text.strip(),
            expected_sentence='',
            is_exact_match=False,
            typing_duration_ms=typing_duration,
            total_keystrokes=self.keystroke_count,
            backspace_count=self.backspace_count,
            submission_time=int(import('time').time() * 1000)
        )
        
        if hasattr(app, 'db'): 
            app.db.insert_emotion_label(emotion_label)

        current_game = app.user_data.get('current_game', 1)

        if hasattr(app, 'db'):
            app.db.flush_keystroke_buffer()
            
        print(f" level {current_game} saved. emoji selected : {self.selected_emoji}")
        print(f"   Participant: {task_data['participant_id']}")
        print(f"   Session: {task_data['session_id']}")
        print(f"   Task Type: {task_data['task_type']}")
        print(f"   Typed: {task_data['typed_text'][:30]}...")
        
        # Navigation (debriefing after games 5,6)
        if current_game in Strings.DEBRIEFING_AFTER_GAMES :
            self.manager.current = f'debriefing_{self.task_type}'

        elif current_game == 7:
            # Set session end time on final task
            app.user_data['session_end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.manager.current = 'completion'

        else:
            # app.user_data['current_game'] = current_game + 1
            # self.manager.current = f'game_{current_game + 1}_{Strings.GAME_SEQUENCE[current_game]}'
            next_game_num = current_game + 1
            
            app.user_data['current_game'] = next_game_num
            
            next_emotion = Strings.GAME_SEQUENCE[next_game_num - 1]
            next_screen_name = f'game_{next_game_num}_{next_emotion}'
            
            print(f" Navigating to: {next_screen_name}")
            if self.manager.has_screen(next_screen_name):
                self.manager.current = next_screen_name
            else:
                self.manager.current = self.manager.next()
    
    def get_backend_data(self):
        """
        Get all collected data formatted for backend submission
        
        Returns:
            dict: Complete session data ready for backend API
        """
        app = App.get_running_app()
        
        return {
            'participant_id': app.user_data.get('participant_id', ''),
            'session_id': app.user_data.get('session_id', ''),
            'session_start_time': app.user_data.get('session_start_time', ''),
            'session_end_time': app.user_data.get('session_end_time', ''),
            'tasks': app.user_data.get('tasks', [])
        }

    def on_keystroke(self, keystroke: KeystrokeEvent):
        """
        Receives keystrokes from CustomKeyboard
        - Updates visible text
        - Stores keystroke in DB
        """

        app = App.get_running_app()

        # Handle special keys
        if keystroke.key_id == 'key_backspace':
            self.backspace(None)
            keystroke.is_backspace = True
            self.backspace_count += 1

        elif keystroke.key_id == 'key_done':
            # Optional: trigger submit
            return

        else:
            self.add_char(keystroke.key_char)

        self.keystroke_count += 1
        # Store keystroke in database
        if hasattr(app, 'db'):
            app.db.insert_keystroke(keystroke)
            
