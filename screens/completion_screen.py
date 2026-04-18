# screens/completion_screen.py 

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.widget import Widget

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings, PixelUI, BASE_PATH
from screens.pixel_ui_wrapper import PixelFrame
from screens.utils import generate_session_id, load_participant_data
import os


class CompletionScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(CompletionScreen, self).__init__(**kwargs)
        
        # Create pixel frame wrapper with custom layout
        # Title with stars, then mushroom handsdown, then content
        self.pixel_frame = PixelFrame(
            title='THANK YOU! ',
            show_stars=True,
            show_header=True,
            show_quit=False,
            show_reset=False
        )
        
        # Add mushroom handsdown below title (in the main container)
        self._add_mushroom_below_title()
        
        # Main content layout (preserved structure)
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(8), dp(6), dp(8), dp(8)],
            spacing=dp(8)
        )
        
        # Completion confirmation
        self.complete_msg = self.create_subtitle(
            'You completed all 7 games successfully!',
            color=Colors.TEXT_BLACK,
            wrap=False
        )
        self.complete_msg.font_name = PixelUI.FONT_BODY
        self.complete_msg.font_size = Typography.PIXEL_BODY_LARGE
        self.complete_msg.halign = 'center'
        self.complete_msg.valign = 'middle'
        self.complete_msg.size_hint_y = None
        self.complete_msg.height = dp(58)
        self.complete_msg.bind(
            size=lambda i, v: setattr(i, 'text_size', (v[0], v[1]))
        )
        main_layout.add_widget(self.complete_msg)
        
        # Session Summary Box
        summary_container = self.create_card(
            size_hint=(1, 1),
            padding=dp(12),
            bg_color=Colors.BACKGROUND_LIGHT_BLUE
        )
        
        summary_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            padding=[dp(6), dp(6), dp(6), dp(6)]
        )
        
        summary_title = self.create_title(
            'Session Summary',
            size='standard',
            color=Colors.PRIMARY_BLUE
        )
        summary_title.font_name = PixelUI.FONT_TITLE
        summary_title.font_size = Typography.PIXEL_TITLE_SMALL
        summary_title.height = dp(58)

        
        # Dynamic stats label - will be updated in on_enter
        self.stats_label = self.create_subtitle('Loading stats...', color=Colors.TEXT_BLACK, wrap=False)
        self.stats_label.font_name = PixelUI.FONT_BODY
        self.stats_label.font_size = Typography.PIXEL_BODY_SMALL
        self.stats_label.halign = 'left'
        self.stats_label.valign = 'top'
        self.stats_label.size_hint = (1, 1)
        self.stats_label.bind(
            size=lambda i, v: setattr(i, 'text_size', (max(v[0] - dp(8), 0), v[1]))
        )

        # Keep title at top and stats directly below.
        summary_layout.add_widget(summary_title)
        summary_layout.add_widget(self.stats_label)
        summary_container.add_widget(summary_layout)
        main_layout.add_widget(summary_container)
        

        # Buttons: ONLY Replay and Close (Export completely removed per requirements)
        buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=Layout.BUTTON_HEIGHT_STANDARD + Layout.SPACING_STANDARD,
            spacing=Layout.SPACING_STANDARD,
            padding=(dp(2), 0)
        )
        
        # REPLAY button (50% width since export removed)
        replay_btn = self.create_button(
            text=Strings.BTN_REPLAY,
            on_press=self.on_replay,
            button_type='success'
        )
        replay_btn.size_hint_x = 0.5
        buttons_layout.add_widget(replay_btn)
        
        # CLOSE APP button (50% width)
        close_btn = self.create_button(
            text=Strings.BTN_CLOSE,
            on_press=self.on_close,
            button_type='danger'
        )
        close_btn.size_hint_x = 0.5
        close_btn.background_color = Colors.DANGER_RED_DARK
        buttons_layout.add_widget(close_btn)
        
        main_layout.add_widget(buttons_layout)
        
        # Set content to pixel frame
        self.pixel_frame.set_content(main_layout)
        self.add_widget(self.pixel_frame)

    def _add_mushroom_below_title(self):
        """Add mushroom handsdown image below the title"""
        source = os.path.join(BASE_PATH, 'assets', 'ui', 'mushroom_handsdown.png')
        if not os.path.exists(source):
            return
        
        # Create a horizontal layout for the mushroom below title
        mushroom_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(10),
            padding=[dp(20), dp(5)]
        )
        
        # Center the mushroom
        mush_img = Image(
            source=source,
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={'center_x': 0.5}
        )
        
        mushroom_row.add_widget(Widget())  # Left spacer
        mushroom_row.add_widget(mush_img)
        mushroom_row.add_widget(Widget())  # Right spacer
        
        # Insert after title bar (index 1, after title at index 0)
        # The main_container is the second child of PixelFrame (after background)
        if hasattr(self.pixel_frame, 'main_container'):
            self.pixel_frame.main_container.add_widget(mushroom_row, index=1)
    
    def on_enter(self):
        """Update stats when screen is entered"""
        super().on_enter()
        
        # Get dynamic stats from session
        app = App.get_running_app()

        user_data = app.user_data if hasattr(app,'user_data') else {}

        completed_games = user_data.get('completed_games',set())
        games_completed = len(completed_games)
        
        tasks = app.user_data.get('tasks', [])
        total_keystrokes = sum(len(t.get('typed_text', '')) for t in tasks)

        # Get total sessions from persistent storage
        participant_data = load_participant_data()
        total_sessions = participant_data.get('total_sessions', 1)
        participant_id = app.user_data.get('participant_id', 'Unknown')
        
        # Calculate session time if available
        session_start = app.user_data.get('session_start_time', '')
        session_end = app.user_data.get('session_end_time', '')
        if session_start and session_end:
            from datetime import datetime
            try:
                start = datetime.strptime(session_start, "%Y-%m-%d %H:%M:%S")
                end = datetime.strptime(session_end, "%Y-%m-%d %H:%M:%S")
                duration = end - start
                minutes = int(duration.total_seconds() / 60)
                session_time = f"{minutes} minutes"
            except:
                session_time = "5 minutes"
        else:
            session_time = "5 minutes"
        
        # UI text
        if games_completed == 7:
            self.complete_msg.text = 'CONGRATULATIONS! You completed all 7 levels successfully'
        elif games_completed > 0:
            self.complete_msg.text = f'You completed {games_completed} levels out of 7 levels.'
        else:
            self.complete_msg.text = 'Session ended. No levels completed.'
        
        # Update stats text
        stats_text = (
            f"- {games_completed} levels completed\n"
            f"- {session_time} total time\n"
            f"- Participant ID:\n  {participant_id}\n"
            f"- Total sessions: {total_sessions}"
        )
        
        self.stats_label.text = stats_text
        
        print(f" Completion screen showing: {games_completed} levels, {total_keystrokes} keystrokes")
    
    def on_replay(self, instance):
        """Replay game - skip to instructions with new session ID"""
        app = App.get_running_app()

        participant_id = app.user_data.get('participant_id')
        demographics = app.user_data.get('demographics', {})
        
        # Generate new session ID
        # session_id = generate_session_id() //redundant
        
        # Reset user data
        app.user_data = {
            'participant_id': participant_id,
            'demographics': demographics,
            'session_id': None, #session_id,
            'current_game': 0,
            'tasks': [],
            'debriefing_complete': False
        }
        
        print(f" REPLAY pressed")
        self.manager.current = 'instructions'
    
    def on_close(self, instance):
        """Close the entire app"""
        print("Session closed")
        App.get_running_app().stop()

        
