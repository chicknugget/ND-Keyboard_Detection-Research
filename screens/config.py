# screens/config.py
"""
Centralized configuration for all screens
Colors, dimensions, fonts, and Android configuration
"""

from kivy.metrics import dp, sp
from kivy.core.window import Window
import platform



class Colors:
    """Standard color palette for the app"""
    
    # Primary Colors
    PRIMARY_BLUE = (0.2, 0.4, 0.8, 1)       
    PRIMARY_BLUE_DARK = (0.12, 0.45, 0.75, 1)  
    
    # Success/Action Colors
    SUCCESS_GREEN = (0.25, 0.7, 0.25, 1)    
    SUCCESS_GREEN_LIGHT = (0.3, 0.75, 0.3, 1)
    
    # Warning/Alert Colors
    WARNING_ORANGE = (0.8, 0.4, 0.2, 1)     
    WARNING_GOLD = (1, 0.8, 0, 1)           
    
    # Error/Danger Colors
    DANGER_RED = (1, 0, 0, 1)               
    DANGER_RED_DARK = (0.7, 0.3, 0.3, 1)    
    
    # Background Colors
    BACKGROUND_WHITE = (1, 0.95, 0.95, 1)         
    BACKGROUND_LIGHT_GRAY = (0.95, 0.95, 0.95, 1)  
    BACKGROUND_LIGHT_BLUE = (0.95, 0.97, 1, 1)     
    
    # Text Colors
    TEXT_BLACK = (0, 0, 0, 1)               
    TEXT_GRAY = (0.5, 0.5, 0.5, 1)          
    TEXT_LIGHT_GRAY = (0.1, 0.1, 0.1, 1)    
    
    # UI Element Colors
    DISABLED_GRAY = (0.55, 0.55, 0.55, 1)   
    DISABLED_GRAY_LIGHT = (0.6, 0.6, 0.6, 1)
    EMOJI_BUTTON_DEFAULT = (0.9, 0.9, 0.9, 1)  
    EMOJI_BUTTON_SELECTED = (0.3, 0.8, 0.3, 1)  
    
    # Export/Info Colors
    INFO_BLUE = (0.2, 0.6, 0.9, 1)          


class Layout:
    """Standard layout dimensions"""
    
    # Padding & Spacing
    PADDING_STANDARD = dp(20)
    PADDING_LARGE = dp(25)
    PADDING_SMALL = dp(10)
    PADDING_CARD = dp(15)
    
    SPACING_STANDARD = dp(10)
    SPACING_LARGE = dp(15)
    SPACING_SMALL = dp(10)
    SPACING_TINY = dp(8)
    
    # Button Dimensions
    BUTTON_HEIGHT_LARGE = dp(50)
    BUTTON_HEIGHT_STANDARD = dp(44)
    BUTTON_HEIGHT_SMALL = dp(36)
    BUTTON_HEIGHT_TINY = dp(30)
    
    # Input Field Dimensions
    INPUT_HEIGHT = dp(40)
    CHECKBOX_SIZE = dp(28)
    
    # Card/Container Dimensions
    CARD_RADIUS = dp(12)
    CARD_PADDING = dp(15)
    
    # Title/Header Heights
    TITLE_HEIGHT = dp(40)
    SUBTITLE_HEIGHT = dp(20)
    HEADER_HEIGHT = dp(40)


class Typography:
    """Standard font sizes"""
    
    # Title Sizes
    TITLE_LARGE = sp(24)
    TITLE_STANDARD = sp(20)
    TITLE_SMALL = sp(18)
    
    # Body Text Sizes
    BODY_LARGE = sp(18)
    BODY_STANDARD = sp(16)
    BODY_SMALL = sp(15)
    BODY_TINY = sp(14)
    
    # Button Text Sizes
    BUTTON_LARGE = sp(15)
    BUTTON_STANDARD = sp(12)
    BUTTON_SMALL = sp(10)
    
    # Special Text Sizes
    EMOJI_SIZE = sp(30)



# ANDROID CONFIGURATION

class AppConfig:
    """App-wide configuration settings"""
    
    # Screen Orientation
    ORIENTATION = 'portrait'  # Options: 'portrait', 'landscape', 'all'
    
    # Mobile Screen Dimensions 
    MOBILE_WIDTH = 360  # dp
    MOBILE_HEIGHT = 640  # dp
    
    # Text wrapping width for mobile
    TEXT_WRAP_WIDTH = dp(300)
    
    @staticmethod
    def lock_orientation(orientation='portrait'):
        """
        Lock screen orientation on Android
        
        Args:
            orientation (str): 'portrait', 'landscape', or 'all'
        """
        try:
            if platform.system() == 'Android':
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                ActivityInfo = autoclass('android.content.pm.ActivityInfo')
                
                activity = PythonActivity.mActivity
                
                if orientation == 'portrait':
                    activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT)
                elif orientation == 'landscape':
                    activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE)
                else:
                    activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED)
                    
                print(f" Screen orientation locked to: {orientation}")
            else:
                print(f" Orientation locking only works on Android (current: {platform.system()})")
                
        except Exception as e:
            print(f" Could not lock orientation: {e}")
    
    @staticmethod
    def set_window_size_mobile():
        """Set window size to simulate mobile screen (for PC testing)"""
        if platform.system() != 'Android':
            Window.size = (AppConfig.MOBILE_WIDTH, AppConfig.MOBILE_HEIGHT)
            print(f" Window resized to {AppConfig.MOBILE_WIDTH}x{AppConfig.MOBILE_HEIGHT} (mobile simulation)")



# COMMON TEXT/STRINGS

class Strings:
    """Common text strings used across the app"""
    
    # Game sequence (7 games)
    GAME_SEQUENCE = ['relaxation', 'happy', 'boredom', 'sad', 'frustrated', 'stress','relaxation_final']
    UNIQUE_EMOTIONS = ['relaxation', 'happy', 'boredom', 'sad', 'frustrated', 'stress']
    
    # Debriefing triggers
    DEBRIEFING_AFTER_GAMES = [5,6]  # After frustrated (game 5) and stress (game 6)
    
    # Fixed emojis for all feedback screens
    FIXED_EMOJIS = [
        {
            'id': 'relaxation',
            'source': 'assets/emojis/relaxation.png'
        },
        {
            'id': 'happy',
            'source': 'assets/emojis/happy.png'
        },
        {
            'id': 'sad',
            'source': 'assets/emojis/sad.png'
        },
        {
            'id': 'frustrated',
            'source': 'assets/emojis/frustrated.png'
        },
        {
            'id': 'stress',
            'source': 'assets/emojis/stress.png'
        },
        {
            'id': 'boredom',
            'source': 'assets/emojis/boredom.png'
        }
    ]
    
    # Button labels
    BTN_QUIT = 'QUIT'
    BTN_CONTINUE = 'CONTINUE'
    BTN_SUBMIT = 'SUBMIT'
    BTN_RESET = 'RESET'
    BTN_DECLINE = 'DECLINE'
    BTN_CONSENT = 'I CONSENT'
    BTN_START = 'START GAME'
    BTN_UNDERSTAND = 'I UNDERSTAND - CONTINUE'
    BTN_EXPORT = 'EXPORT DATA'
    BTN_CLOSE = 'CLOSE APP'
    BTN_REPLAY = 'REPLAY'

def init_app_config():
    """
    Initialize app configuration (call this in main.py)
    Sets orientation lock and window size
    """
    AppConfig.lock_orientation(AppConfig.ORIENTATION)
    # Uncomment the line below to set mobile window size for PC testing
    AppConfig.set_window_size_mobile()
