from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.clock import Clock
from datetime import datetime
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.properties import NumericProperty, StringProperty

from games.shuffle import ShufflingGame
from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography

GAME_SETTINGS = {
    'relaxation': {'rigged': None, 'speed': 0.65, 'no_of_glasses': 3, 'points_show': False, 'total_rounds': 2},
    'happy':      {'rigged': "rig_win", 'speed': 0.5, 'no_of_glasses': 3, 'points_show': True, 'total_rounds': 2},
    'boredom':    {'rigged': None, 'speed': 0.5, 'no_of_glasses': 1, 'points_show': True, 'total_rounds': 2},
    'sad':        {'rigged': "rig_nwin_oloss", 'speed': 0.5, 'no_of_glasses': 4, 'points_show': True, 'total_rounds': 2},
    'frustrated': {'rigged': "rig_owin_nloss", 'speed': 0.4, 'no_of_glasses': 5, 'points_show': True,  'total_rounds': 2},
    'stress':     {'rigged': "rig_lose", 'speed': 0.35, 'no_of_glasses': 6, 'points_show': True, 'total_rounds': 2},
    'relaxation_final': {'rigged': None, 'speed': 0.65, 'no_of_glasses': 3, 'points_show': False, 'total_rounds': 2}
}

class GameContainerScreen(BaseScreen):
    def __init__(self, game_number=7, total_games=7, emotion='relaxation_final', **kwargs):
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
        
       
        self.header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=Layout.BUTTON_HEIGHT_SMALL,
            spacing=Layout.SPACING_SMALL,
            # Hide header entirely if Level 7
            opacity=1 if self.game_number < 7 else 0,
            disabled=True if self.game_number >= 7 else False
        )
        
        progress_text = self.create_subtitle(
            f'Level {self.game_number}/{self.total_games}',
            color=Colors.PRIMARY_BLUE
        )
        progress_text.font_size = Typography.BODY_STANDARD
        progress_text.bold = True
        progress_text.size_hint_x = None
        progress_text.width = Layout.BUTTON_HEIGHT_LARGE * 1.5
        self.header.add_widget(progress_text)
        
        progress_container = BoxLayout(orientation='vertical', size_hint_x=1)
        progress_bg = BoxLayout(size_hint=(1, None), height=Layout.SPACING_LARGE)
        
        with progress_bg.canvas.before:
            Color(*Colors.DISABLED_GRAY_LIGHT)
            progress_bg.bg_rect = RoundedRectangle(pos=progress_bg.pos, size=progress_bg.size, radius=[Layout.SPACING_SMALL])
        progress_bg.bind(pos=lambda i, v: setattr(progress_bg.bg_rect, 'pos', v),
                         size=lambda i, v: setattr(progress_bg.bg_rect, 'size', v))
        
        progress_percentage = self.game_number / self.total_games
        self.progress_fill = BoxLayout(size_hint=(None, None), width=0, height=Layout.SPACING_LARGE)
        progress_bg.bind(width=lambda inst, val: setattr(self.progress_fill, 'width', val * progress_percentage))

        with self.progress_fill.canvas.before:
            Color(*Colors.DANGER_RED_DARK)
            self.progress_fill.fill_rect = RoundedRectangle(pos=self.progress_fill.pos, size=self.progress_fill.size, radius=[Layout.SPACING_SMALL])
        self.progress_fill.bind(pos=lambda i, v: setattr(self.progress_fill.fill_rect, 'pos', v),
                                size=lambda i, v: setattr(self.progress_fill.fill_rect, 'size', v))
        
        progress_bg.add_widget(self.progress_fill)
        progress_container.add_widget(progress_bg)
        self.header.add_widget(progress_container)
        
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
            total_rounds=config['total_rounds']
        )
        
        self.game_placeholder.add_widget(your_game)

    def on_leave(self):
        self.end_time = datetime.now()

    def go_to_post_task(self):
        if self.game_number == 7:
            self.manager.current = 'completion'
        else:
            self.manager.current = f'post_task_{self.emotion}'
    
    def on_quit(self, instance):
        self.manager.current = 'completion'
