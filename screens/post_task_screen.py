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

from screens.config import SoundManager


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
        super(PostTaskScreen, self).__init__(
            enable_wrapper=True,
            title='FEEDBACK',
            show_stars=True,         
            show_header=True,
            show_quit=False,
            show_reset=False, **kwargs
        )
        self.task_type = task_type

        # Main vertical layout — all proportional
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(6), dp(4), dp(6), dp(4)],
            spacing=dp(5)
        )

        # 1. INSTRUCTION SUBTITLE 
        instruction_label = Label(
            text=(
                'Please provide your feedback below.\n'
                'Type any ONE of the sentences below, type at least 16 characters.'
                'You can provide your own thoughts.'
            ),

            font_name=PixelUI.FONT_BODY,
            font_size=Typography.BUTTON_SMALL,
            color=Colors.TEXT_BLACK,
            halign='center',
            valign='middle',
            size_hint_y=0.12
        )
        instruction_label.bind( width=lambda i, v: setattr(i, 'text_size', (v, None)))

        main_layout.add_widget(instruction_label)





        # 2. SENTENCES CARD (scrollable so it doesn't overflow) 
        sentences_scroll_content = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[dp(6), dp(4)],
            spacing=dp(2)
        )
        sentences_scroll_content.bind(
            minimum_height=sentences_scroll_content.setter('height')
        )

        sentences_text = '\n'.join([f"{i+1}. {s}" for i, s in enumerate(SENTENCE_OPTIONS)])
        sentences_label = Label(
            text=sentences_text,
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.PIXEL_BODY_STANDARD,
            color=Colors.TEXT_BLACK,
            bold=True,
            halign='left',
            valign='top',
            size_hint_y=None
        )
        sentences_label.bind(
            width=lambda i, v: setattr(i, 'text_size', (v, None)),
            texture_size=lambda i, v: setattr(i, 'height', v[1])
        )
        sentences_scroll_content.add_widget(sentences_label)

        sentences_card = self.create_scrollable_content(
            sentences_scroll_content, size_hint=(1, 0.24)
        )
        main_layout.add_widget(sentences_card)

        # 3. INPUT BOX 
        self.typed_display = self.create_input_field(
            hint_text='Start Typing...',
            multiline=True
        )
        self.typed_display.font_name = PixelUI.FONT_BODY
        self.typed_display.size_hint_y = 0.10       # override the 0.08 from factory
        self.typed_display.keyboard_mode = 'managed'
        self.typed_display.is_focusable = True
        self.typed_display.bind(height=lambda inst, val: setattr(inst, 'font_size', Typography.PIXEL_BODY_LARGE))
        self.typed_display.bind(text=self.on_text_change)
        self.typed_display.bind(focus=self.on_text_focus)
        main_layout.add_widget(self.typed_display)

        # 4. CHARACTER COUNTER 
        self.char_counter = Label(
            text=f'0 / {MIN_TYPING_LENGTH} characters (minimum)',
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.PIXEL_BODY_SMALL,
            color=Colors.DISABLED_GRAY,
            size_hint_y=0.04,
            halign='right',
            valign='middle'
        )
        self.char_counter.bind(size=self.char_counter.setter('text_size'))
        main_layout.add_widget(self.char_counter)

        # 5. CUSTOM KEYBOARD (always visible)
        self.keyboard_placeholder = self.create_card(
            size_hint=(1, 0.32),
            padding=dp(1)
        )
        self.keyboard = CustomKeyboard()
        self.keyboard_placeholder.add_widget(self.keyboard)

        main_layout.add_widget(self.keyboard_placeholder)


        # 6. DONE BUTTON 
        self.done_btn = self.create_button(
            text='DONE',
            on_press=self.on_done_pressed,
            button_type='success',
            disabled=True
        )
        self.done_btn.size_hint_y = 0.08
        self.done_btn.background_color = Colors.DISABLED_GRAY

        main_layout.add_widget(self.done_btn)

        # Set content
        self.set_content(main_layout)


        # ── Emoji popup state (built lazily on first use) ──
        self._emoji_popup = None
        self._submit_btn_popup = None
        self._popup_emoji_buttons = []
    

    
    def on_enter(self):
        """Reset for fresh task"""
        super().on_enter() if hasattr(super(), 'on_enter') else None
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
        self.char_counter.color = Colors.DISABLED_GRAY
        self.done_btn.disabled = True
        self.done_btn.background_color = Colors.DISABLED_GRAY

        self.emoji_click_history = []
        self.keystroke_count = 0
        self.backspace_count = 0

        # Dismiss emoji popup if open
        if self._emoji_popup:
            self._emoji_popup.dismiss()
            self._emoji_popup = None
        self.show_title()

        print(f"PostTaskScreen({self.task_type}) reset")


    def on_text_focus(self, instance, focused):
        """Keyboard is always visible now — nothing to show/hide on focus"""

        if focused:
            self.typing_start_time = int(__import__('time').time() * 1000)


    



    def on_text_change(self, instance, value):
        self.typed_length = len(value)
        self.char_counter.text = f'{self.typed_length} / {MIN_TYPING_LENGTH} characters (minimum)'

        if self.typed_length >= MIN_TYPING_LENGTH:
            self.char_counter.color = Colors.SUCCESS_GREEN
            self.done_btn.disabled = False
            self.done_btn.background_color = Colors.SUCCESS_GREEN
        else:
            self.char_counter.color = Colors.WARNING_ORANGE
            self.done_btn.disabled = True
            self.done_btn.background_color = Colors.DISABLED_GRAY
            self.selected_emoji = ''

    
    def on_done_pressed(self, instance):
        """Show emoji selection popup when DONE is pressed"""
        from kivy.uix.popup import Popup
        from kivy.uix.floatlayout import FloatLayout

        SoundManager.play('positive')

        # Defocus keyboard
        self.typed_display.focus = False

        # Build popup content
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(16)
        )

        # Title
        emoji_title = Label(
            text='Select your feelings :',
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.PIXEL_BODY_STANDARD,
            color=Colors.WARNING_ORANGE,
            bold=True,
            size_hint_y=None,
            height=dp(30),
            halign='center',
            valign='middle'
        )
        emoji_title.bind(size=emoji_title.setter('text_size'))
        content.add_widget(emoji_title)

        # Emoji grid — 2 cols, 3 rows
        self._popup_emoji_buttons = []
        emoji_grid = GridLayout(
            cols=2,
            size_hint_y=None,
            height=dp(270),
            spacing=dp(10),
            padding=dp(6)
        )

        for emoji in Strings.FIXED_EMOJIS:
            btn = EmojiImageButton(
                source=emoji['source'],
                size_hint=(1, None),
                height=dp(85),
                opacity=1.0
            )
            btn.emoji_id = emoji['id']
            btn.bind(on_press=lambda x, e=emoji['id']: self._popup_select_emoji(e))
            emoji_grid.add_widget(btn)
            self._popup_emoji_buttons.append(btn)

        content.add_widget(emoji_grid)

        # Submit button — disabled until emoji selected
        self._submit_btn_popup = Button(
            text=Strings.BTN_SUBMIT,
            size_hint_y=None,
            height=dp(44),
            background_normal='',
            background_color=Colors.DISABLED_GRAY,
            disabled=True,
            on_press=self._on_popup_submit
        )
        content.add_widget(self._submit_btn_popup)

        self._emoji_popup = Popup(
            title='',
            content=content,
            size_hint=(0.88, 0.75),
            auto_dismiss=False,
            separator_height=0
        )
        self._emoji_popup.open()

    def _popup_select_emoji(self, emoji_id):
        """Handle emoji selection inside popup — hide others, activate submit"""
        # SoundManager.play('tick')
        SoundManager.play('yeay')
        self.selected_emoji = emoji_id
        self.emoji_click_history.append(emoji_id)

        # Hide all other emoji buttons — keep only the selected one
        for btn in self._popup_emoji_buttons:
            if btn.emoji_id == emoji_id:
                btn.opacity = 1.0
                btn.disabled = False
            else:
                btn.opacity = 0       # disappear unselected ones
                btn.disabled = True

        # Activate submit button
        if self._submit_btn_popup:
            self._submit_btn_popup.disabled = False
            self._submit_btn_popup.background_color = Colors.SUCCESS_GREEN

    def _on_popup_submit(self, instance):
        """Dismiss emoji popup and run on_submit logic"""
        SoundManager.play('positive')
        if self._emoji_popup:
            self._emoji_popup.dismiss()
            self._emoji_popup = None
        # Delegate to the existing on_submit which handles all backend + navigation
        self.on_submit(instance)
    
    # def select_emoji(self, emoji_id):
    #     self.selected_emoji = emoji_id
    #     self.emoji_click_history.append(emoji_id)   # record every tap
    #     # Reset all to muted
    #     for btn in self.emoji_buttons:
    #         btn.opacity = 0.8
    #     # Highlight selected
    #     for btn in self.emoji_buttons:
    #         if btn.emoji_id == emoji_id:
    #             btn.opacity = 1.0
    #             break
    #     # Enable submit
    #     self.submit_btn.disabled = False
    #     self.submit_btn.background_color = Colors.SUCCESS_GREEN
    
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
        typing_duration = int(__import__('time').time() * 1000) - getattr(self, 'typing_start_time', 0)
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
            submission_time=int(__import__('time').time() * 1000)
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
            app.user_data['session_end_time'] = int(__import__('time').time() * 1000)
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
        else:
            self.add_char(keystroke.key_char)

        self.keystroke_count += 1
        keystroke.position_in_sentence = len(self.typed_display.text)
        # Store keystroke in database
        if hasattr(app, 'db'):
            app.db.insert_keystroke(keystroke)
            
