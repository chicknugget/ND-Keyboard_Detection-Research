
# screens/instructions_screen.py 

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from datetime import datetime

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings
from screens.utils import generate_session_id, reset_app_data, increment_session_count

from data.models import Session

class InstructionsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(InstructionsScreen, self).__init__(**kwargs)
        
        main_layout = BoxLayout(
            orientation='vertical',
            padding=Layout.PADDING_STANDARD,
            spacing=Layout.SPACING_STANDARD
        )
        
        # Header bar  
        header = self.create_header_bar(show_quit=True, show_reset=True, on_reset=self.on_reset )
        main_layout.add_widget(header)

        # Title
        title = self.create_title(' Instructions', size='standard')
        main_layout.add_widget(title)


        # Scrollable instructions card
        instructions_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[Layout.PADDING_SMALL, Layout.PADDING_SMALL],
            spacing=Layout.SPACING_SMALL
        )
        instructions_layout.bind(minimum_height=instructions_layout.setter('height'))
        
        # Dynamic instructions text with user data
        app = App.get_running_app()
        user_data = getattr(app, 'user_data', {})
        demographics = user_data.get('demographics', {})
        
        instructions_text = f"""
            WHAT YOU'LL DO:
            • There are 7 levels of this game. Each level lasts ~1 minute
            • You will give feedback after each level 
            • Select emojis that match your feelings
            • Try to stay relaxed and focused

            IMPORTANT:
            • Some games are intentionally HARD
            • Take your time typing - don't rush
            • All data is COMPLETELY ANONYMOUS
            • You can quit anytime

            YOUR INFO:
            ID: {user_data.get('participant_id', 'Not set')}
            Age: {demographics.get('age_range', 'Not selected')}
            Gender: {demographics.get('gender', 'Not selected')}

            Ready to begin? Click START GAME!
        """
        
        instructions_label = self.create_subtitle(instructions_text, color=Colors.TEXT_BLACK)
        instructions_label.font_size = Typography.BODY_SMALL
        instructions_label.halign = 'left'
        instructions_label.valign = 'top'
        instructions_label.size_hint_y = None
        
        def set_text_size(instance, value):
            instance.text_size = (value, None)
        
        instructions_label.bind(
            width=set_text_size,
            texture_size=lambda i, v: setattr(i, 'height', v[1])
        )
        
        instructions_layout.add_widget(instructions_label)
        
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
        
        self.add_widget(main_layout)
    
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
