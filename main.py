from kivy.config import Config
Config.set('graphics', 'resizable', True)

import os
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.resources import resource_add_path 
from kivy.properties import NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
import shutil

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
            
        sm.add_widget(CompletionScreen(name='completion')

        return sm
    
    def export_debug(self, instance):
        try:
            export_dir = self.user_data_dir
            summary_path = os.path.join(export_dir, 'debug_summary.txt')
            db_export_path = os.path.join(export_dir, 'debug_database.db')
            shutil.copy2(self.db.db_path, db_export_path)

            with open(summary_path, 'w') as f:
                f.write("=== DATABASE DEBUG SUMMARY ===\n")
                f.write(f"Export time: {datetime.now()}\n")
                f.write(f"Session ID: {self.user_data.get('session_id', 'No session yet')}\n")
                f.write(f"Keystrokes: {self.db.count_keystrokes(self.user_data.get('session_id', ''))}\n")
                f.write(f"Emotion labels: {len(self.db.get_emotion_labels(self.user_data.get('session_id', '')))}\n")
                f.write(f"Database path: {self.db.db_path}\n")
                f.write(f"Export path: {export_dir}\n")
            
            print(f"Debug export saved to: {summary_path}")
            self.debug_btn.text = "Exported!"
        except Exception as e:
            print(f"Debug export failed: {e}")
            self.debug_btn.text = "Export Failed"
    

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


