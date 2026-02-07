import time

from kivy.app import Appfrom kivy.uix.screenmanager import screenmanager
from kivy.core.window import Window

from data.database import DatabaseManager
from data.models import Session

from screens.config import init_app_config, Stringsfrom screens.consent_screen import consent_screen
from screens.demographics_screen import DemographicsScreen 
from screens.instructions_screen import instructions_screen
from screens.game_container_screen import GameContainerScreen 
from screens.post_task_screen import PostTaskScreen 
from screens.debriefing_screen import debriefing_screen 
from screens.completion_screen import CompletionScreen 

Window.size = (400, 700)

class EmotionStudyApp(App):
    def build(self): #required method by kivy: creates and returns the main widget
        self.user_data = {} #intializes an empty dictionary to store session information

        sm = ScreenManager() #making a screenmanager that will hold all screens and handle navigation
        sm.add_widget(consent_screen(name = 'consent'))
        '''
        .add_widget = adds a child widget
        ConsentScreen() = creates a new instance of consent screen class
        name='consent' = a parameter we pass to create a screen: it gives the screen a unique name

        Take the ScreenManager (sm), and add to it a new ConsentScreen object that has the name 'consent'
        '''
        sm.add_widget(DemographicsScreen(name='demographics'))
        sm.add_widget(InstructionsScreen(name='instructions'))

        for i, emotion in enumerate(Strings.GAME_SEQUENCE):
            game_num = i + 1
            sm.add_widget(GameContainerScreen(name=f'game_{game_num}_{emotion}', game_number=game_num, emotion=emotion))
            sm.add_widget(PostTaskScreen(name=f'post_task__{emotion}', task_type=emotion))

        sm.add_widget(DebriefingScreen(name='debriefing_frustrated'))

        sm.add_widget(CompletionScreen(name='completion'))

        return sm

    def on_start(self):
        self.db = DatabaseManager()
        print("Database initialized!")

    def on_stop(self):
        if hasattr(self, 'db'):
            self.db.close()
            print("Database closed!")


if name=='main':
    init_app_config() #calls the function from config.py that sets up app configurations
    EmotionStudyApp().run() #creates an instance of the app and runs it