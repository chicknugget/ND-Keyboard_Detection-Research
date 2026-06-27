# screens/instructions_screen.py

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings, PixelUI
from screens.utils import generate_session_id, reset_app_data, increment_session_count

from data.models import Session
import time


from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

class InstructionsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(InstructionsScreen, self).__init__(
            enable_wrapper=True,
            title='Instructions',
            show_stars=True,
            show_header=True,
            show_quit=True,
            show_reset=True,
            on_reset=self.on_reset,**kwargs)
        instructions_label_text = """
Welcome!

Thank you for taking part in our study. Before you begin, please take a moment to read the instructions below.

ABOUT THE GAME

- Your goal is to guess which cup is hiding the ball.
- Each correct guess earns you +10 points.
- Each incorrect guess deducts 10 points.
- The game consists of 7 levels, with each level lasting about 1 minute.
- Your score carries over across all 7 levels.
- If you complete all 7 levels and finish with at least 100 points, you will receive a surprise reward from us.

WHAT YOU WILL DO

- Play through all 7 levels of the game.
- After each level, write a short comment about your experience.
- Choose the emoji that best matches how you felt while playing that level.

PLEASE KEEP IN MIND

- Some levels are intentionally more challenging than others.
- There are no right or wrong answers. We are interested in your genuine experience.
- Take your time while playing and while writing your feedback. There is no need to rush.
- Your typing patterns and responses are collected anonymously and used only for academic research.
- You are free to quit the game at any time if you no longer wish to continue.

We hope you enjoy the game, and we appreciate your participation.

When you are ready, click START GAME to begin.
"""
        
        self.instructions_text = instructions_label_text
        
        # Original main layout (preserved exactly)
        main_layout = BoxLayout(
            orientation='vertical',
            padding=Layout.PADDING_STANDARD,
            spacing=Layout.SPACING_STANDARD
        )

        # Scrollable instructions card
        instructions_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[Layout.PADDING_SMALL, Layout.PADDING_SMALL],
            spacing=Layout.SPACING_SMALL
        )
        instructions_layout.bind(minimum_height=instructions_layout.setter('height'))
        
        # Placeholder label — text populated in on_enter so it always shows current data
                # Standard Kivy Label without the hidden base_screen bindings
        self.instructions_label = Label(
            text='',
            color=Colors.TEXT_BLACK,
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.PIXEL_BODY_STANDARD, # Or PIXEL_BODY_SMALL
            halign='left',
            valign='top',
            size_hint_y=None,
            markup=True
        )

        # Clean bindings just for text wrapping and height calculation
        self.instructions_label.bind(
            width=lambda instance, value: setattr(instance, 'text_size', (value, None)),
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        
        instructions_layout.add_widget(self.instructions_label)
        
        # Create scrollable card
        card = self.create_scrollable_content(instructions_layout, size_hint=(1, 0.50))
        main_layout.add_widget(card)
        
        main_layout.add_widget(BoxLayout(size_hint_y= 0.03))
        
        # Start button 
        start_btn = self.create_button(
            text=Strings.BTN_START,
            on_press=self.on_start_study,
            button_type='primary'
        )
        start_btn.size_hint_y = 0.07
        main_layout.add_widget(start_btn)
        
        # Set content to main layout
        self.set_content(main_layout)

    def on_enter(self):
        """Refresh dynamic text every time the screen is shown (e.g. after a reset)."""
        # this is to create and DISPLAY the new participant id each time reset
        
        super().on_enter() if hasattr(super(), 'on_enter') else None
        app = App.get_running_app()
        user_data = getattr(app, 'user_data', {})
        demographics = user_data.get('demographics', {})

        self.instructions_label.text = self.instructions_text


    def on_start_study(self, instance):
        """Generate session ID and start first game"""
        app = App.get_running_app()
        
        # Generate new session ID
        session_id = generate_session_id()
        app.user_data['session_id'] = session_id
        app.user_data['current_game'] = 1  # Start with game 1
        
        # Record session start time
        session_start_time = int( time.time() * 1000)
        app.user_data['session_start_time'] = session_start_time
        
        # Increment session count in persistent storage
        total_sessions = increment_session_count()

        session = Session(
            session_id=session_id,
            participant_id=app.user_data.get('participant_id', 'Not set'),
            start_time=session_start_time,
            end_time=None,   
            status='in_progress',
            screen_width=app.root.width,
            screen_height=app.root.height,
            age_range=app.user_data.get('demographics', {}).get('age_range', ''),
            gender=app.user_data.get('demographics', {}).get('gender', ''),
        )

        if hasattr(app, 'db') and app.db:
            app.db.insert_session(session)
        else:
            print("warning...")
        
        print(f" GAME STARTED! Session ID: {session_id} (Total sessions: {total_sessions})")
        print(f" Session start time: {session_start_time}")
        print(f" User: {app.user_data}")
        
        # Navigate to first game (game 1: relaxed)
        self.manager.current = 'game_1_relaxation'
    
    def on_reset(self, instance):
        """Show confirmation popup before resetting"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        content.add_widget(Label(
            text='Are you sure you want to reset?\nAll progress will be lost.',
            color=Colors.TEXT_BLACK,
            halign='center',
            valign='middle'
        ))
        content.children[0].bind(size=content.children[0].setter('text_size'))

        btn_row = BoxLayout(spacing=dp(10), size_hint_y=0.4)

        popup = Popup(
            title='Confirm Reset',
            content=content,
            size_hint=(0.7, 0.35),
            auto_dismiss=False
        )

        def do_reset(*_):
            popup.dismiss()
            app = App.get_running_app()
            app.user_data = reset_app_data()
            self.instructions_label.text = ''
            print(" App reset - returning to consent screen")
            self.manager.current = 'consent'

        yes_btn = Button(text='Yes, Reset', on_press=do_reset)
        no_btn = Button(text='Cancel', on_press=lambda *_: popup.dismiss())

        btn_row.add_widget(yes_btn)
        btn_row.add_widget(no_btn)
        content.add_widget(btn_row)

        popup.open()
    
