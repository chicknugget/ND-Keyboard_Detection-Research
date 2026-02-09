# main.py - Complete 7-Game Flow Implementation

"""
Emotion Study App - Complete Implementation
 7-game sequence: relaxed → happy → sad → frustrated → stressed → bored → relaxed
 Debriefing after games 4 (frustrated) and 5 (stressed)
 Participant ID (persistent across app launches)
 Session ID (new per game playthrough)
 Reset functionality
 Quit functionality
 Replay functionality
"""

import time
import os 
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.resources import resource_add_path 
from kivy.properties import NumericProperty

from data.database import DatabaseManager
from data.models import Session

from screens.consent_screen import ConsentScreen
from screens.demographics_screen import DemographicsScreen
from screens.instructions_screen import InstructionsScreen
from screens.post_task_screen import PostTaskScreen
from screens.debriefing_screen import DebriefingScreen
from screens.completion_screen import CompletionScreen
from screens.game_container_screen import GameContainerScreen

from screens.config import init_app_config, Strings
from screens.utils import init_app_data


# --- PERSON B INTEGRATION: Asset Path ---
# Assuming your images are in ./assets/cup_ball
cup_ball_image_path = os.path.join(os.path.dirname(__file__), 'assets', 'cup_ball')
resource_add_path(cup_ball_image_path)

Window.size = (400, 700)


class EmotionStudyApp(App):

    # --- PERSON B INTEGRATION: Shared Points ---
    total_points = NumericProperty(0)

    user_data = {}
    
    def build(self):
        # Initialize app configuration (orientation lock, etc.)
        init_app_config()
        
        # Initialize user data with participant ID
        self.user_data = init_app_data()
        
        # Create screen manager
        sm = ScreenManager()
        
        # MAIN FLOW
        sm.add_widget(ConsentScreen(name='consent'))
        sm.add_widget(DemographicsScreen(name='demographics'))
        sm.add_widget(InstructionsScreen(name='instructions'))
        
        # GAME CYCLE
        
        #game container screens
        for i, emotion in enumerate(Strings.GAME_SEQUENCE, 1):
            game_num = i
            
            sm.add_widget(GameContainerScreen(
                name=f'game_{game_num}_{emotion}', 
                game_number=game_num, 
                emotion=emotion,
                total_games=len(Strings.GAME_SEQUENCE)
            ))
        #feedbackscreen
            sm.add_widget(PostTaskScreen(
                name=f'post_task_{emotion}',
                task_type=emotion
            ))
        
        # debriefing screen
            if game_num in Strings.DEBRIEFING_AFTER_GAMES:
                sm.add_widget(DebriefingScreen(name=f'debriefing_{emotion}'))
        
    # completionscreen
        sm.add_widget(CompletionScreen(name='completion'))
        
        # ===== STARTING SCREEN =====
        # Check if first time or returning user
        if self.user_data.get('is_first_time', True):
            sm.current = 'consent'  # First time: start from consent
            print(" First-time user - starting from consent screen")
        else:
            sm.current = 'instructions'  # Returning: skip to instructions
            print(" Returning user - starting from instructions screen")
        
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


