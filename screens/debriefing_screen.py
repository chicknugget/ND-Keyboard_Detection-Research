
# screens/debriefing_screen.py 
"""
Debriefing Screen: ONLY after frustrated (game 4) and stressed (game 5) 
 Cannot press BACK
 Cannot tap outside
 Must click "I Understand"
 Reassuring task explanation
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.core.window import Window

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings


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
    
    def __init__(self, **kwargs):
        super(DebriefingScreen, self).__init__(**kwargs)
        
        main_layout = BoxLayout(
            orientation='vertical',
            padding=Layout.PADDING_STANDARD,
            spacing=Layout.SPACING_STANDARD
        )

        # Title with warning color
        title = self.create_title(
            '*** IMPORTANT MESSAGE ***',
            size='small',
            color=Colors.WARNING_GOLD
        )
        main_layout.add_widget(title)
        
        # Reassuring message card
        message_text = """
The task you just completed was INTENTIONALLY impossible.

     No one was watching your performance
     Nothing negative was recorded about you  
     All "threats" and messages were FAKE
     This was part of the research design

You did PERFECTLY! 

Thank you for participating. Take a deep breath.

     Our team appreciates you
        """
        
        # Create card 
        card = self.create_card(
            size_hint=(0.95, None),
            padding=Layout.CARD_PADDING,
            bg_color=Colors.BACKGROUND_WHITE
        )
        card.pos_hint = {'center_x': 0.5}
        card.bind(minimum_height=card.setter('height'))
        
        message_label = self.create_subtitle(message_text, color=Colors.TEXT_LIGHT_GRAY)
        message_label.font_size = Typography.BODY_STANDARD
        message_label.halign = 'center'
        message_label.valign = 'top'
        message_label.text_size = (None, None)
        message_label.size_hint_y = None
        message_label.bind(
            texture_size=lambda i, v: setattr(i, 'height', v[1])
        )

        card.add_widget(message_label)
        main_layout.add_widget(card)

        # Spacer
        main_layout.add_widget(BoxLayout(size_hint_y=None, height=Layout.PADDING_SMALL))
        
        # "I Understand" button (cannot skip)
        understand_btn = self.create_button(
            text=Strings.BTN_UNDERSTAND,
            on_press=self.on_understand,
            button_type='primary'
        )
        main_layout.add_widget(understand_btn)
        
        self.add_widget(main_layout)
    
    def on_understand(self, instance):
        """ONLY way to exit - proceed to next game or completion"""
        app = App.get_running_app()
        if not hasattr(app, 'user_data'):
            app.user_data = {}

        app.user_data['debriefing_complete'] = True
        current_game = app.user_data.get('current_game', 1)
  
        print(f" Debriefing acknowledged (after game {current_game})")
        
        # Navigation: continue to next game
        # After game 4 debriefing → go to game 5 
        # After game 5 debriefing → go to game 6 
        if current_game == 4:
            app.user_data['current_game'] = 5
            self.manager.current = 'game_5_stressed'
        elif current_game == 5:
            app.user_data['current_game'] = 6
            self.manager.current = 'game_6_bored'
        else:
            # Fallback
            print("⚠️ Unexpected debriefing state")
            self.manager.current = 'completion'
