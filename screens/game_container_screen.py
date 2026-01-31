
# screens/game_container_screen.py 
"""
Game Container: Progress tracking + game placeholder
 Level X of 7 + ProgressBar
 Person B game placeholder + completion callback
 Full mobile layout
 Quit button
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.app import App
from kivy.clock import Clock
from datetime import datetime

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings


class GameContainerScreen(BaseScreen):
    def __init__(self, game_number=1, total_games=7, emotion='relaxed', **kwargs):
        super(GameContainerScreen, self).__init__(**kwargs)
        self.game_number = game_number
        self.total_games = total_games
        self.emotion = emotion
        
        main_layout = BoxLayout(
            orientation='vertical',
            padding=Layout.PADDING_STANDARD,
            spacing=Layout.PADDING_STANDARD
        )
        
        # Header bar with quit button and progress bar
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=Layout.BUTTON_HEIGHT_SMALL,
            spacing=Layout.SPACING_SMALL,
            padding=[Layout.PADDING_SMALL, Layout.PADDING_SMALL, Layout.PADDING_SMALL, 0]
        )
        
        # Progress text (left side) - "Level X/7"
        progress_text = self.create_subtitle(
            f'Level {self.game_number}/{self.total_games}',
            color=Colors.PRIMARY_BLUE
        )
        progress_text.font_size = Typography.BODY_STANDARD
        progress_text.bold = True
        progress_text.size_hint_x = None
        progress_text.width = Layout.BUTTON_HEIGHT_LARGE * 1.5
        progress_text.halign = 'left'
        header.add_widget(progress_text)
        
        # Modern Progress Bar (center) - shows completed games out of 7
        progress_container = BoxLayout(
            orientation='vertical',
            size_hint_x=1
        )
        
        # Progress bar background (gray rounded rectangle)
        from kivy.graphics import Color, RoundedRectangle, Rectangle
        progress_bg = BoxLayout(
            size_hint=(1, None),
            height=Layout.SPACING_LARGE
        )
        
        with progress_bg.canvas.before:
            Color(*Colors.DISABLED_GRAY_LIGHT)
            progress_bg.bg_rect = RoundedRectangle(
                pos=progress_bg.pos,
                size=progress_bg.size,
                radius=[Layout.SPACING_SMALL]
            )
        
        progress_bg.bind(
            pos=lambda i, v: setattr(progress_bg.bg_rect, 'pos', v),
            size=lambda i, v: setattr(progress_bg.bg_rect, 'size', v)
        )
        
        # Progress bar fill (blue rounded rectangle) - shows current task progress
        # Calculate percentage: (current game number / total games)
        progress_percentage = self.game_number / self.total_games
        
        self.progress_fill = BoxLayout(
            size_hint=(None, None),
            width=0,  # Will be set dynamically
            height=Layout.SPACING_LARGE
        )
        
        # Bind to parent to calculate actual pixel width
        def update_progress_width(instance, value):
            # Calculate actual pixel width based on percentage
            if hasattr(progress_bg, 'width'):
                actual_width = progress_bg.width * progress_percentage
                self.progress_fill.width = max(0, actual_width)  # At least 0 pixels
        
        progress_bg.bind(width=update_progress_width)

        
        with self.progress_fill.canvas.before:
            Color(*Colors.PRIMARY_BLUE_DARK)
            self.progress_fill.fill_rect = RoundedRectangle(
                pos=self.progress_fill.pos,
                size=self.progress_fill.size,
                radius=[Layout.SPACING_SMALL]
            )
        
        self.progress_fill.bind(
            pos=lambda i, v: setattr(self.progress_fill.fill_rect, 'pos', v),
            size=lambda i, v: setattr(self.progress_fill.fill_rect, 'size', v)
        )
        
        progress_bg.add_widget(self.progress_fill)
        progress_container.add_widget(progress_bg)
        
        header.add_widget(progress_container)
        
        # Quit button 
        quit_btn = Button(
            text='QUIT',
            size_hint=(None, 1),
            width=Layout.BUTTON_HEIGHT_STANDARD * 1.5,
            background_color=Colors.DANGER_RED_DARK,
            font_size=Typography.BUTTON_SMALL,
            on_press=self.on_quit
        )
        header.add_widget(quit_btn)
        
        main_layout.add_widget(header)
        
        # Title: "Task X: Emotion"
        self.task_label = self.create_title(
            f'Level {self.game_number}',
            size='standard'
        )
        self.task_label.height = Layout.HEADER_HEIGHT
        main_layout.add_widget(self.task_label)
        
        # GAME PLACEHOLDER (Person B integrates here)
        self.game_placeholder = BoxLayout(
            orientation='vertical',
            size_hint_y=1,  # Take most of the space
            padding=Layout.PADDING_CARD
        )
        
        placeholder_label = self.create_subtitle(
            f'[PERSON B GAME PLACEHOLDER]\\n\\nTask {self.game_number}: {self.emotion.capitalize()} Game',
            color=Colors.TEXT_GRAY
        )
        placeholder_label.font_size = Typography.BODY_STANDARD
        placeholder_label.halign = 'center'
        self.game_placeholder.add_widget(placeholder_label)
        
        main_layout.add_widget(self.game_placeholder)
        
        # Complete button at the bottom
        self.complete_button = self.create_button(
            text='COMPLETE GAME',
            on_press=self.fake_game_complete,
            button_type='success'
        )
        main_layout.add_widget(self.complete_button)
        
        self.add_widget(main_layout)
    
    def fake_game_complete(self, instance):
        """TESTING: Simulates Person B game completion"""
        app = App.get_running_app()
        
        print(f" Game {self.game_number} ({self.emotion}) completed!")
        
        # Wait a moment then go to post-task screen
        Clock.schedule_once(lambda dt: self.go_to_post_task(), 1.0)
    
    def go_to_post_task(self):
        """Navigate to appropriate post-task screen"""
        # Go to post_task screen for this emotion
        post_task_screen = f'post_task_{self.emotion}'
        print(f"  Navigating to {post_task_screen}")
        self.manager.current = post_task_screen
    
    def on_quit(self, instance):
        """Override quit button to navigate to completion screen instead of closing app"""
        app = App.get_running_app()
        tasks_completed = len(app.user_data.get('tasks', []))
        
        # Record session end time (only if session has started)
        if 'session_start_time' in app.user_data:
            session_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            app.user_data['session_end_time'] = session_end_time
            print(f" Session end time: {session_end_time}")
        
        print(f" Quit pressed - navigating to completion screen")
        print(f" Tasks completed: {tasks_completed} out of 7")
        
        # Navigate to completion screen (will show 0 tasks if no games completed)
        self.manager.current = 'completion'
