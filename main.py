import time
import os
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.resources import resource_add_path
from kivy.properties import NumericProperty

# --- PERSON B INTEGRATION: Imports ---
from data.database import DatabaseManager
from data.models import Session
from screens.config import init_app_config, Strings
from screens.consent_screen import ConsentScreen
from screens.demographics_screen import DemographicsScreen 
from screens.instructions_screen import InstructionsScreen
from screens.game_container_screen import GameContainerScreen 
from screens.post_task_screen import PostTaskScreen 
from screens.debriefing_screen import DebriefingScreen 
from screens.completion_screen import CompletionScreen 

# --- PERSON B INTEGRATION: Asset Path ---
# Assuming your images are in ./assets/cup_ball
cup_ball_image_path = os.path.join(os.path.dirname(__file__), 'assets', 'cup_ball')
resource_add_path(cup_ball_image_path)

Window.size = (400, 700)

class EmotionStudyApp(App):
    # --- PERSON B INTEGRATION: Shared Points ---
    total_points = NumericProperty(0)

    def build(self):
        self.user_data = {}

        sm = ScreenManager()
        
        # Initial Screens
        sm.add_widget(ConsentScreen(name='consent'))
        sm.add_widget(DemographicsScreen(name='demographics'))
        sm.add_widget(InstructionsScreen(name='instructions'))

    
        for i, emotion in enumerate(Strings.GAME_SEQUENCE, start=1):
            game_num = i
            
            sm.add_widget(GameContainerScreen(
                name=f'game_{game_num}_{emotion}', 
                game_number=game_num, 
                emotion=emotion,
                total_games=len(Strings.GAME_SEQUENCE)
            ))
            
            # This serves as your FeedbackScreen
            sm.add_widget(PostTaskScreen(
                name=f'post_task_{emotion}', 
                task_type=emotion
            ))
            
            if game_num in Strings.DEBRIEFING_AFTER_GAMES:
                sm.add_widget(DebriefingScreen(name=f'debriefing_{emotion}'))

        # # Final Screens
        game_num += 1
        sm.add_widget(GameContainerScreen(
                name='game_7_relaxation_final', 
                game_number=game_num, 
                emotion='relaxation_final',
                total_games=7
            ))
        sm.add_widget(CompletionScreen(name='completion'))

        return sm

    def on_start(self):
        self.db = DatabaseManager()
        print("Database initialized!")

    def on_stop(self):
        if hasattr(self, 'db'):
            self.db.close()
            print("Database closed!")

if __name__ == '__main__':
    init_app_config()
    EmotionStudyApp().run()
