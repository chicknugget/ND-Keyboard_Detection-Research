
# screens/game_container_screen.py 


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.clock import Clock
from datetime import datetime

from kivy.graphics import Color, Rectangle, RoundedRectangle

from games.shuffle import ShufflingGame

from screens.base_screen import BaseScreen
from data.models import GameResult
from screens.config import Colors, Layout, Typography


GAME_SETTINGS = {
    'relaxation': {'rigged': None, 'speed': 0.65, 'no_of_glasses': 3, 'points_show': False, 'total_rounds': 1, 'bg_music':'relaxation'},
    'happy':      {'rigged': "rig_win", 'speed': 0.5, 'no_of_glasses': 3, 'points_show': True, 'total_rounds': 5, 'bg_music':'happy'},
    'boredom':    {'rigged': None, 'speed': 0.5, 'no_of_glasses': 1, 'points_show': True, 'total_rounds': 5, 'bg_music':'boredom'},
    'sad':        {'rigged': "rig_nwin_oloss", 'speed': 0.5, 'no_of_glasses': 4, 'points_show': True, 'total_rounds': 5, 'bg_music':'sad'},
    'frustrated': {'rigged': "rig_owin_nloss", 'speed': 0.4, 'no_of_glasses': 5, 'points_show': True,  'total_rounds': 5, 'bg_music':'frustrated'},
    'stress':     {'rigged': "rig_lose", 'speed': 0.35, 'no_of_glasses': 6, 'points_show': True, 'total_rounds': 5, 'bg_music':'stress'},
    'relaxation_final': {'rigged': "rig_win", 'speed': 0.65, 'no_of_glasses': 3, 'points_show': True, 'total_rounds': 5, 'bg_music':'relaxation'}
}


class GameContainerScreen(BaseScreen):
    def __init__(self, game_number=1, total_games=7, emotion='relaxation_final', **kwargs):
        super(GameContainerScreen, self).__init__(**kwargs)
        self.game_number = game_number
        self.total_games = total_games
        self.emotion = emotion

        with self.canvas.before:
            Color(97/255, 112/255, 44/255, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        main_layout = BoxLayout(
            orientation='vertical',
            padding=Layout.PADDING_SMALL,
            spacing=0
        )
        
        # Header bar 
        self.header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=Layout.BUTTON_HEIGHT_SMALL,
            spacing=Layout.SPACING_SMALL,
            padding=[Layout.PADDING_SMALL, Layout.PADDING_SMALL, Layout.PADDING_SMALL, 0]
        )
        
        # # Progress text (left side) - "Level X/7"
        # progress_text = self.create_subtitle(
        #     f'Level {self.game_number}/{self.total_games}',
        #     color=Colors.DANGER_RED_DARK
        # )
        # progress_text.font_size = Typography.BODY_STANDARD
        # progress_text.bold = True
        # progress_text.size_hint_x = None
        # progress_text.width = Layout.BUTTON_HEIGHT_LARGE * 1.5

        # self.header.add_widget(progress_text)

        # --- Level Badge with background like QUIT button ---
        level_badge = Button(
            text=f'Level {self.game_number}/{self.total_games}',
            size_hint=(None, 1),
            width=Layout.BUTTON_HEIGHT_LARGE * 1.6,
            background_color=Colors.DANGER_RED_DARK,
            color=(1, 1, 1, 1),
            font_size=Typography.BUTTON_SMALL,
            bold=True
        )
        self.header.add_widget(level_badge)
        

        progress_container = BoxLayout(orientation='vertical', size_hint_x=1)
        progress_bg = BoxLayout(size_hint=(1,None), height = Layout.SPACING_LARGE)
        
        with progress_bg.canvas.before:
            Color(*Colors.DISABLED_GRAY_LIGHT)
            progress_bg.bg_rect = RoundedRectangle(pos=progress_bg.pos, size=progress_bg.size, radius=[Layout.SPACING_SMALL])
        progress_bg.bind(pos=lambda i, v: setattr(progress_bg.bg_rect, 'pos', v),
                         size=lambda i, v: setattr(progress_bg.bg_rect, 'size', v))
        
        progress_percentage = min(self.game_number / self.total_games ,1)
        
        self.progress_fill = BoxLayout(size_hint=(None, None), height=Layout.SPACING_LARGE)

        def update_progress(*args):
            self.progress_fill.width = progress_bg.width * progress_percentage
        
        progress_bg.bind(width =update_progress)
        Clock.schedule_once(update_progress)

        
        with self.progress_fill.canvas.before:
            Color(*Colors.DANGER_RED_DARK)
            self.progress_fill.fill_rect = RoundedRectangle(pos=self.progress_fill.pos, size=self.progress_fill.size, radius=[Layout.SPACING_SMALL])
        self.progress_fill.bind(pos=lambda i, v: setattr(self.progress_fill.fill_rect, 'pos', v),
                                size=lambda i, v: setattr(self.progress_fill.fill_rect, 'size', v))   
        
        progress_bg.add_widget(self.progress_fill)
        progress_container.add_widget(progress_bg)
        
        self.header.add_widget(progress_container)
        
        # Quit button 
        quit_btn = Button(
            text='QUIT',
            size_hint=(None, 1),
            width=Layout.BUTTON_HEIGHT_STANDARD * 1.5,
            background_color=Colors.DANGER_RED_DARK,
            font_size=Typography.BUTTON_SMALL,
            on_press=self.on_quit
        )
        self.header.add_widget(quit_btn)
        main_layout.add_widget(self.header)

        

        self.game_placeholder = BoxLayout(
            orientation='vertical',
            size_hint_y=1,
            padding=0
        )
        
        main_layout.add_widget(self.game_placeholder)
        
        self.add_widget(main_layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_pre_enter(self):
        self.start_time = datetime.now()
        self.game_placeholder.clear_widgets()
        
        config = GAME_SETTINGS.get(self.emotion, GAME_SETTINGS['relaxation_final'])
        
        your_game = ShufflingGame(
            level=self.game_number,
            rigged=config['rigged'],
            speed=config['speed'],
            no_of_glasses=config['no_of_glasses'],
            points_show=config['points_show'],
            total_rounds=config['total_rounds'],
            bg_music=config.get('bg_music', 'relaxation'),
            on_game_complete=self.go_to_post_task
        )
        
        self.game_placeholder.add_widget(your_game)

    def on_leave(self):
        self.end_time = datetime.now()
        # app = App.get_running_app()
        # app.user_data['last_game_end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def go_to_post_task(self):
        """Navigate to appropriate post-task screen"""

        end_time = int(__import__('time').time() * 1000)
        start_time = int(self.start_time.timestamp() * 1000)
        app = App.get_running_app()
        game_result = GameResult(
            session_id=app.user_data.get('session_id', ''),
            task_type=self.emotion,
            final_score=app.total_points,
            outcome='completed',
            start_time=start_time,
            end_time=end_time,
            duration_ms=end_time - start_time,
            attempts=1
        )

        if hasattr(app, 'db'):
            app.db.insert_game_result(game_result)
        if self.game_number == 7:
            self.manager.current = 'completion'
            app.db.update_session(app.user_data.get('session_id', ''), status='completed', end_time=end_time)
            print(f"  Navigating to completion")

        else :
            self.manager.current = f'post_task_{self.emotion}'
            print(f"  Navigating to post_task_{self.emotion}")

    
    def on_quit(self, instance):
        """Override quit button to navigate to completion screen instead of closing app"""

        for widget in self.game_placeholder.children:
            if hasattr(widget, 'bg_music') and widget.bg_music:
                widget.bg_music.stop()

        app = App.get_running_app()
        tasks_completed = len(app.user_data.get('tasks', []))
        
        
        # Record session end time (only if session has started)
        if 'session_start_time' in app.user_data:
            session_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            app.user_data['session_end_time'] = session_end_time
            print(f" Session end time: {session_end_time}")
        
        print(f" Quit pressed - navigating to completion screen")
        print(f" Tasks completed: {tasks_completed} out of 7")

        if hasattr(app, 'db'):
            app.db.update_session(
                app.user_data.get('session_id', ''), status='quit', 
                                  end_time=int(__import__('time').time() * 1000))
        
        # Navigate to completion screen (will show 0 tasks if no games completed)
        self.manager.current = 'completion'
