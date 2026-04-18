# screens/instructions_screen.py

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from datetime import datetime

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings, PixelUI
from screens.pixel_ui_wrapper import PixelFrame
from screens.utils import generate_session_id, reset_app_data, increment_session_count

from data.models import Session
import time

class InstructionsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(InstructionsScreen, self).__init__(**kwargs)
        
        # Create pixel frame wrapper
        self.pixel_frame = PixelFrame(
            title='Instructions',
            show_stars=True,
            show_header=True,
            show_quit=True,
            show_reset=True,
            on_reset=self.on_reset
        )
        
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
        self.instructions_label = self.create_subtitle('', color=Colors.TEXT_BLACK)
        self.instructions_label.font_name = PixelUI.FONT_BODY
        self.instructions_label.font_size = Typography.PIXEL_BODY_SMALL
        self.instructions_label.halign = 'left'
        self.instructions_label.valign = 'top'
        self.instructions_label.size_hint_y = None
        
        def set_text_size(instance, value):
            instance.text_size = (value, None)
        
        self.instructions_label.bind(
            width=set_text_size,
            texture_size=lambda i, v: setattr(i, 'height', v[1])
        )
        
        instructions_layout.add_widget(self.instructions_label)
        
        # Create scrollable card
        card = self.create_scrollable_content(instructions_layout, size_hint=(1, 0.45))
        main_layout.add_widget(card)
        
        main_layout.add_widget(BoxLayout(size_hint_y=None, height=Layout.PADDING_SMALL))
        
        # Start button 
        start_btn = self.create_button(
            text=Strings.BTN_START,
            on_press=self.on_start_study,
            button_type='primary'
        )
        main_layout.add_widget(start_btn)
        
        # Set content to pixel frame
        self.pixel_frame.set_content(main_layout)
        self.add_widget(self.pixel_frame)

    def on_enter(self):
        """Refresh dynamic text every time the screen is shown (e.g. after a reset)."""
        # this is to create and DISPLAY the new participant id each time reset
        
        super().on_enter() if hasattr(super(), 'on_enter') else None
        app = App.get_running_app()
        user_data = getattr(app, 'user_data', {})
        demographics = user_data.get('demographics', {})

        self.instructions_label.text = (
            "WHAT YOU'LL DO:\n"
            "- There are 7 levels of this game. Each level lasts about 1 minute\n"
            "- You will give feedback after each level\n"
            "- Select emojis that match your feelings\n"
            "- Try to stay relaxed and focused\n\n"
            "IMPORTANT:\n"
            "- Some games are intentionally hard\n"
            "- Take your time typing, do not rush\n"
            "- All data is completely anonymous\n"
            "- You can quit anytime\n\n"
            "YOUR INFO:\n"
            f"ID: {user_data.get('participant_id', 'Not set')}\n"
            f"Age: {demographics.get('age_range', 'Not selected')}\n"
            f"Gender: {demographics.get('gender', 'Not selected')}\n\n"
            "Ready to begin? Click START GAME!"
        )
    
    def on_start_study(self, instance):
        """Generate session ID and start first game"""
        app = App.get_running_app()
        
        # Generate new session ID
        session_id = generate_session_id()
        app.user_data['session_id'] = session_id
        app.user_data['current_game'] = 1  # Start with game 1
        
        # Record session start time
        session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        app.user_data['session_start_time'] = session_start_time
        
        # Increment session count in persistent storage
        total_sessions = increment_session_count()

        session = Session(
            session_id=session_id,
            participant_id=app.user_data.get('participant_id', 'Not set'),
            start_time=session_start_time,
            end_time=session_start_time,   
            status='in_progress'  
        )

        app.db.insert_session(session)
        
        print(f" GAME STARTED! Session ID: {session_id} (Total sessions: {total_sessions})")
        print(f" Session start time: {session_start_time}")
        print(f" User: {app.user_data}")
        
        # Navigate to first game (game 1: relaxed)
        self.manager.current = 'game_1_relaxation'
    
    def on_reset(self, instance):
        """Reset app data and return to consent screen"""
        app = App.get_running_app()
        
        # Reset everything
        app.user_data = reset_app_data()
        
        print(" App reset - returning to consent screen")
        self.manager.current = 'consent'
 
