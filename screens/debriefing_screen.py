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
from screens.pixel_ui_wrapper import PixelFrame
import os


class DebriefingScreen(BaseScreen):

    # Block BACK button
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        Window.bind(on_keyboard=self._block_back)

    def on_pre_leave(self, *args):
        super().on_pre_leave(*args)
        Window.unbind(on_keyboard=self._block_back)

    def _block_back(self, window, key, *args):
        if key == 27:  # Android BACK button
            return True  # block it
        return False
    
    #UI component
    def __init__(self, **kwargs):
        super(DebriefingScreen, self).__init__(**kwargs)
        
        # Create pixel frame wrapper with title and stars
        self.pixel_frame = PixelFrame(
            title='IMPORTANT MESSAGE',
            show_stars=True,
            show_header=True,
            show_quit=False,
            show_reset=False
        )
        
        main_layout = BoxLayout(
            orientation='vertical',
            padding=Layout.PADDING_STANDARD,
            spacing=dp(8)
        )

        # Place 3 mushrooms in the top row (as marked).
        main_layout.add_widget(self._build_top_mushroom_row())
        
        message_text = (
            "The level you just finished was intentionally impossible.\n\n"
            "No one was watching your performance.\n"
            "All warnings and messages were fake.\n"
            "This was part of the game design.\n\n"
            "You did perfectly.\n\n"
            "Thank you for participating. Take a deep breath.\n\n"
            "Our team appreciates you."
        )
        
        card = self.create_card(
            size_hint=(1, None),
            height=dp(340),
            padding=[dp(16), dp(16), dp(16), dp(12)],
            bg_color=Colors.BACKGROUND_WHITE
        )
        card.pos_hint = {'center_x': 0.5}
        
        message_label = self.create_subtitle(message_text, color=Colors.TEXT_LIGHT_GRAY, wrap=False)
        message_label.font_name = PixelUI.FONT_BODY
        message_label.font_size = Typography.PIXEL_BODY_STANDARD
        message_label.halign = 'left'
        message_label.valign = 'top'
        message_label.size_hint = (1, 1)
        message_label.bind(
            size=lambda i, v: setattr(i, 'text_size', (max(v[0] - dp(8), 0), v[1]))
        )


        card.add_widget(message_label)
        main_layout.add_widget(card)

        main_layout.add_widget(BoxLayout(size_hint_y=None, height=Layout.PADDING_SMALL))
        
        # "I Understand" button (cannot skip)
        understand_btn = self.create_button(
            text=Strings.BTN_UNDERSTAND,
            on_press=self.on_understand,
            button_type='primary'
        )
        main_layout.add_widget(understand_btn)
        
        # Set content to pixel frame
        self.pixel_frame.set_content(main_layout)
        self.add_widget(self.pixel_frame)

    def _build_top_mushroom_row(self):
        """Build 3 mushrooms row above message card."""
        row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(76),
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
                height=dp(68),
                allow_stretch=True,
                keep_ratio=True
            )
            row.add_widget(mush)

        return row

    #screen navigation
    def on_understand(self, instance):
        """ONLY way to exit - proceed to next game or completion"""
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

# # screens/debriefing_screen.py 
# """
# Debriefing Screen: ONLY after frustrated (game 5) and stress (game 6) 
#  Cannot press BACK
#  Cannot tap outside
#  Must click "I Understand"
#  Reassuring task explanation
# """

# from kivy.uix.boxlayout import BoxLayout
# from kivy.app import App
# from kivy.core.window import Window

# from screens.base_screen import BaseScreen
# from screens.config import Colors, Layout, Typography, Strings


# class DebriefingScreen(BaseScreen):

#     # Block BACK button
#     def on_pre_enter(self, *args):
#         super().on_pre_enter(*args)
#         Window.bind(on_keyboard=self._block_back)

#     def on_pre_leave(self, *args):
#         super().on_pre_leave(*args)
#         Window.unbind(on_keyboard=self._block_back)

#     def _block_back(self, window, key, *args):
#         if key == 27:  # Android BACK button
#             return True  # block it
#         return False
    
#     #UI component
#     def __init__(self, **kwargs):
#         super(DebriefingScreen, self).__init__(**kwargs)
        
#         main_layout = BoxLayout(
#             orientation='vertical',
#             padding=Layout.PADDING_STANDARD,
#             spacing=Layout.SPACING_STANDARD
#         )

#         title = self.create_title(
#             '*** IMPORTANT MESSAGE ***',
#             size='small',
#             color=Colors.WARNING_GOLD
#         )
#         main_layout.add_widget(title)
        
#         message_text = """
# The Level you just finished was INTENTIONALLY impossible.

#      No one was watching your performance  
#      All warnings and messages were FAKE
#      This was part of the game design

# You did PERFECTLY! 

# Thank you for participating. Take a deep breath.

#      Our team appreciates you
#         """
        
#         card = self.create_card(
#             size_hint=(0.95, None),
#             padding=Layout.CARD_PADDING,
#             bg_color=Colors.BACKGROUND_WHITE
#         )
#         card.pos_hint = {'center_x': 0.5}
#         card.bind(minimum_height=card.setter('height'))
        
#         message_label = self.create_subtitle(message_text, color=Colors.TEXT_LIGHT_GRAY)
#         message_label.font_size = Typography.BODY_STANDARD
#         message_label.halign = 'center'
#         message_label.valign = 'top'
#         message_label.text_size = (self.width*.85 , None)
#         message_label.size_hint_y = None

#         message_label.bind(
#             width=lambda i, v: setattr(i, 'text_size', (v, None)),
#             texture_size=lambda i, v: setattr(i, 'height', v[1])
#         )


#         card.add_widget(message_label)
#         main_layout.add_widget(card)

#         main_layout.add_widget(BoxLayout(size_hint_y=None, height=Layout.PADDING_SMALL))
        
#         # "I Understand" button (cannot skip)
#         understand_btn = self.create_button(
#             text=Strings.BTN_UNDERSTAND,
#             on_press=self.on_understand,
#             button_type='primary'
#         )
#         main_layout.add_widget(understand_btn)
        
#         self.add_widget(main_layout)

#     #screen navigation
#     def on_understand(self, instance):
#         """ONLY way to exit - proceed to next game or completion"""
#         app = App.get_running_app()

#         if not hasattr(app, 'user_data'):
#             app.user_data = {}

#         app.user_data['debriefing_complete'] = True
#         #current_game just finished
#         current_game = app.user_data.get('current_game', 1)
  
#         print(f" Debriefing acknowledged (after game {current_game})")
        
#         # Move to next_game
#         next_game = current_game +1

#         if next_game <= len(Strings.GAME_SEQUENCE):
#             app.user_data['current_game'] = next_game
            
#             next_emotion = Strings.GAME_SEQUENCE[next_game -1]
#             next_screen = f'game_{next_game}_{next_emotion}'

#             print(f"navigate to {next_screen}")

#             if self.manager.has_screen(next_screen):
#                 self.manager.current = next_screen
#             else:
#                 print("screen missing, navigate to completion")
#                 self.manager.current = 'completion'

#         else:
#             print("all games comleted ")
#             self.manager.current = 'completion'
