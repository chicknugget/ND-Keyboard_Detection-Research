

# screens/post_task_screen.py 
"""
Post-Task Screen
  "Feedback" title 
 Portrait order: Sentences → Input → Emojis → Keyboard → Submit
 Debriefing navigation after games 4/5
"""

from screens.keyboards.sample_keyboard import SampleKeyboard
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

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings

MIN_TYPING_LENGTH = 5
SENTENCE_OPTIONS = [
    'this game is relaxing.',
    'this game makes me happy.',
    'this game makes me sad.',
    'this game is frustrating.',
    'this game makes me stressed.',
    'this game is boring.'
]

class EmojiImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = True

class PostTaskScreen(BaseScreen):
    task_type = StringProperty('relaxed')
    selected_emoji = StringProperty('')
    typed_length = NumericProperty(0)
    
    def __init__(self, task_type='relaxed', **kwargs):
        super(PostTaskScreen, self).__init__(**kwargs)
        self.task_type = task_type
        
        # Main vertical layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=Layout.PADDING_STANDARD,
            spacing=dp(8)
        )
        
        # Feedback" title 
        header = self.create_header_bar( show_quit=False, show_reset=False, title='Feedback' )
        main_layout.add_widget(header)
        
        # Sentences instruction card 
        sentences_card = self.create_card(
            size_hint=(1, None), 
            height=dp(140),
            padding=dp(10)
        )
        
        sentences_text = '\n'.join([f"{i+1}. {s}" for i, s in enumerate(SENTENCE_OPTIONS)])
        sentences_label = Label(
            text=sentences_text,
            font_size=Typography.BODY_SMALL,
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
            hint_text='Type any one sentence here...',
            multiline=True
        )
        self.typed_display.bind(text=self.on_text_change)
        main_layout.add_widget(self.typed_display)
        
        # Character counter
        self.char_counter = Label(
            text=f'0 / {MIN_TYPING_LENGTH} characters (minimum)',
            font_size=Typography.BODY_TINY,
            color=Colors.WARNING_ORANGE,
            size_hint_y=None,
            height=dp(16),
            halign='right'
            # width will auto-adjust based on text
        )
        main_layout.add_widget(self.char_counter)
        
        #Emoji selection title
        self.emoji_title = Label(
            text='Select your feeling:',
            font_size=Typography.BODY_SMALL,
            color=Colors.TEXT_GRAY,
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
                source=emoji['source'],
                size_hint=(None, None),
                size=(dp(45), dp(45)),
                opacity=0.5
            )
            btn.emoji_id = emoji['id']
            btn.bind(on_press=lambda x, e=emoji['id']: self.select_emoji(e))
            self.emoji_grid.add_widget(btn)
            self.emoji_buttons.append(btn)
        
        main_layout.add_widget(self.emoji_grid)
        
        # ===== 5. KEYBOARD PLACEHOLDER (Person C) =====
        self.keyboard_placeholder = self.create_card(
            size_hint=(1, None),
            height=dp(120),
            padding=dp(4)
        )
        self.keyboard = SampleKeyboard(target_screen=self)  ## Placeholder keyboard
        self.keyboard_placeholder.add_widget(self.keyboard)
        main_layout.add_widget(self.keyboard_placeholder)

        
        # Submit button container
        submit_container = BoxLayout(
            size_hint_y=None,
            height=dp(56),
            padding=(Layout.PADDING_STANDARD, 0)
        )
        self.submit_btn = self.create_button(
            text=Strings.BTN_SUBMIT,
            on_press=self.on_submit,
            button_type='success',
            disabled=True
        )
        submit_container.add_widget(self.submit_btn)
        main_layout.add_widget(submit_container)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        """Reset for fresh task"""
        super().on_enter()
        self.reset_screen()
    
    def reset_screen(self):
        self.typed_display.text = ''
        self.typed_length = 0
        self.selected_emoji = ''
        self.char_counter.text = f'0 / {MIN_TYPING_LENGTH} characters (minimum)'
        self.char_counter.color = Colors.WARNING_ORANGE
        self.emoji_title.opacity = 0.1
        self.emoji_grid.opacity = 0.1
        for btn in self.emoji_buttons:
            btn.opacity = 0.5
            btn.disabled = True
        self.submit_btn.disabled = True
        self.submit_btn.background_color = Colors.DISABLED_GRAY
        print(f"PostTaskScreen({self.task_type}) reset")
    
    def on_text_change(self, instance, value):
        self.typed_length = len(value)
        self.char_counter.text = f'{self.typed_length} / {MIN_TYPING_LENGTH} characters (minimum)'
        
        if self.typed_length >= MIN_TYPING_LENGTH:
            #  ENABLE EMOJIS
            self.char_counter.color = Colors.SUCCESS_GREEN
            self.emoji_title.opacity = 1
            self.emoji_grid.opacity = 1
            for btn in self.emoji_buttons:
                btn.opacity = 0.8
                btn.disabled = False
        else:
            #  DISABLE EMOJIS
            self.char_counter.color = Colors.WARNING_ORANGE
            self.emoji_title.opacity = 0.1
            self.emoji_grid.opacity = 0.1
            for btn in self.emoji_buttons:
                btn.opacity = 0.1
                btn.disabled = True
            self.selected_emoji = ''
            self.submit_btn.disabled = True
            self.submit_btn.background_color = Colors.DISABLED_GRAY
    
    def select_emoji(self, emoji_id):
        self.selected_emoji = emoji_id
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
            'selected_emoji': self.selected_emoji,
            
            # Additional metadata
            'text_length': self.typed_length,
            'task_timestamp': task_timestamp
        }
        
        # Append to tasks list
        app.user_data.setdefault('tasks', []).append(task_data)
        
        current_game = app.user_data.get('current_game', 1)
        print(f" Task {current_game} saved: {self.selected_emoji}")
        print(f"   Participant: {task_data['participant_id']}")
        print(f"   Session: {task_data['session_id']}")
        print(f"   Task Type: {task_data['task_type']}")
        print(f"   Typed: {task_data['typed_text'][:30]}...")
        
        # Navigation (debriefing after games 4+5)
        if current_game in [4, 5]:
            self.manager.current = f'debriefing_{self.task_type}'
        elif current_game == 7:
            # Set session end time on final task
            app.user_data['session_end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.manager.current = 'completion'
        else:
            app.user_data['current_game'] = current_game + 1
            self.manager.current = f'game_{current_game + 1}_{Strings.GAME_SEQUENCE[current_game]}'
    
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
