# screens/debriefing_screen.py 
"""
Debriefing Screen: ONLY after frustrated (game 5) and stress (game 6) 
 Cannot press BACK
 Cannot tap outside
 Must click "I Understand"
 Reassuring task explanation
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.image import Image

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings, PixelUI, BASE_PATH
import os

from screens.config import SoundManager


class DebriefingScreen(BaseScreen):

    # Block BACK button
    def on_pre_enter(self, *args):
        # super().on_pre_enter(*args)
        super().on_pre_enter(*args) if hasattr(super(), 'on_pre_enter') else None
        Window.bind(on_keyboard=self._block_back)

    def on_pre_leave(self, *args):
        super().on_pre_leave(*args)
        Window.unbind(on_keyboard=self._block_back)

    def on_leave(self, *args):
        super().on_leave(*args)
        Window.unbind(on_keyboard=self._block_back)

    def _block_back(self, window, key, *args):
        if key == 27:  # Android BACK button
            return True  # block it
        return False
    
    #UI component
    def __init__(self, **kwargs):
        super(DebriefingScreen, self).__init__(enable_wrapper=True,
                                                title='IMPORTANT MESSAGE',
                                                show_stars=True,
                                                show_header=True,
                                                show_quit=False,
                                                show_reset=False,**kwargs)
        
        main_layout = BoxLayout(
            orientation='vertical',
            padding=Layout.PADDING_STANDARD,
            spacing=dp(8)
        )

        # Place 3 mushrooms in the top row
        main_layout.add_widget(self._build_top_mushroom_row())
        
        message_text = (
            "RELAX\n\n"
            "The level you just finished was intentionally impossible.\n\n"
            "This was part of the game design.\n\n"
            "No one was watching your performance.\n"
            "All warnings and messages were fake.\n"
            "You did perfectly.\n\n"
            "Thank you for participating. Take a deep breath.\n\n"
            "Our team appreciates you."
        )
        
        # Scrollable message card
        message_scroll_content = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[dp(12), dp(8)],
            spacing=dp(4)
        )
        message_scroll_content.bind(
            minimum_height=message_scroll_content.setter('height')
        )

        from kivy.uix.label import Label as KivyLabel
        message_label = KivyLabel(
            text=message_text,
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.PIXEL_BODY_STANDARD,
            color=Colors.TEXT_LIGHT_GRAY,
            halign='left',
            valign='top',
            size_hint_y=None
        )
        message_label.bind(
            width=lambda i, v: setattr(i, 'text_size', (max(v - dp(8), 0), None)),
            texture_size=lambda i, v: setattr(i, 'height', v[1])
        )

        message_scroll_content.add_widget(message_label)

        card = self.create_scrollable_content(
            message_scroll_content, size_hint=(1, 0.55)
        )
        main_layout.add_widget(card)

        main_layout.add_widget(BoxLayout(size_hint_y=0.04))
        
        # "I Understand" button (cannot skip)
        understand_btn = self.create_button(
            text=Strings.BTN_UNDERSTAND,
            on_press=self.on_understand,
            button_type='primary'
        )
        understand_btn.size_hint_y = 0.09
        main_layout.add_widget(understand_btn)
        
        self.set_content(main_layout)

    def _build_top_mushroom_row(self):
        """Build 3 mushrooms row above message card — resizes with window."""
        row = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.18,
            spacing=dp(10),
            padding=[dp(26), 0, dp(26), 0]
        )

        source = os.path.join(BASE_PATH, 'assets', 'ui', 'mushroom_handsup.png')
        if not os.path.exists(source):
            return row

        for _ in range(3):
            mush = Image(
                source=source,
                size_hint=(1, None),
                allow_stretch=True,
                keep_ratio=True
            )
            # Bind height to the row's height so mushrooms scale with window
            row.bind(height=lambda inst, val, m=mush: setattr(m, 'height', val * 0.90))
            row.add_widget(mush)

        return row
    


#add backgroundmusic
    def on_enter(self):
        super().on_enter()
        # SoundManager.play_bg('reward')   # Loops reward_debrief.mp3

    def on_leave(self, *args):
        SoundManager.stop_bg()
        super().on_leave(*args)

    #screen navigation
    def on_understand(self, instance):
        """ONLY way to exit - proceed to next game or completion"""
        SoundManager.play('positive')
        app = App.get_running_app()

        if not hasattr(app, 'user_data'):
            app.user_data = {}

        app.user_data['debriefing_complete'] = True
        #current_game just finished
        current_game = app.user_data.get('current_game', 1)
  
        print(f" Debriefing acknowledged (after game {current_game})")
        
        # Move to next_game
        next_game = current_game +1

        if next_game <= len(Strings.GAME_SEQUENCE):
            app.user_data['current_game'] = next_game
            
            next_emotion = Strings.GAME_SEQUENCE[next_game -1]
            next_screen = f'game_{next_game}_{next_emotion}'

            print(f"navigate to {next_screen}")

            if self.manager.has_screen(next_screen):
                self.manager.current = next_screen
            else:
                print("screen missing, navigate to completion")
                self.manager.current = 'completion'

        else:
            print("all games comleted ")
            self.manager.current = 'completion'
