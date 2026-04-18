# screens/demographics_screen.py 
"""
Demographics Screen: Optional participant info
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.app import App
from kivy.metrics import dp

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings, PixelUI
from screens.pixel_ui_wrapper import PixelFrame
from screens.utils import load_participant_data  # kept for potential future use


class DemographicsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(DemographicsScreen, self).__init__(**kwargs)
        
        # Create pixel frame wrapper
        self.pixel_frame = PixelFrame(
            title='Participant Info',
            show_stars=True,
            show_header=True,
            show_quit=True,
            show_reset=False
        )
        
        # Original main layout (preserved exactly)
        main_layout = BoxLayout(
            orientation='vertical',
            padding=Layout.PADDING_STANDARD,
            spacing=Layout.SPACING_STANDARD
        )
 
        title_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=Layout.TITLE_HEIGHT + Layout.SUBTITLE_HEIGHT,
            spacing=Layout.SPACING_TINY
        )
        
        subtitle = self.create_subtitle('(All fields optional)')
        subtitle.font_name = PixelUI.FONT_BODY
        subtitle.font_size = Typography.PIXEL_BODY_SMALL
        
        title_layout.add_widget(subtitle)
        main_layout.add_widget(title_layout)
        
        # Participant ID - Auto-generated but editable
        id_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=Layout.INPUT_HEIGHT + Layout.SUBTITLE_HEIGHT + Layout.SPACING_SMALL,
            spacing=Layout.SPACING_SMALL
        )
        id_label = self.create_subtitle('Participant ID:', color=Colors.TEXT_BLACK)
        id_label.font_name = PixelUI.FONT_BODY
        id_label.font_size = Typography.PIXEL_BODY_STANDARD
        id_label.size_hint_y = None
        id_label.height = Layout.SUBTITLE_HEIGHT
        
        self.id_input = self.create_input_field(
            hint_text='Auto-generated (or enter custom ID)',
            multiline=False
        )
        self.id_input.font_name = PixelUI.FONT_BODY
        # Text will be populated in on_enter so it always reflects the current participant ID 
        id_layout.add_widget(id_label)
        id_layout.add_widget(self.id_input)
        main_layout.add_widget(id_layout)
        
        # Age Range
        age_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=Layout.INPUT_HEIGHT + Layout.SUBTITLE_HEIGHT + Layout.SPACING_SMALL,
            spacing=Layout.SPACING_SMALL
        )  
        age_label = self.create_subtitle('Age Range:', color=Colors.TEXT_BLACK)
        age_label.font_name = PixelUI.FONT_BODY
        age_label.font_size = Typography.PIXEL_BODY_STANDARD
        age_label.size_hint_y = None
        age_label.height = Layout.SUBTITLE_HEIGHT
        self.age_spinner = Spinner(
            text='Select Age Range',
            values=['15-19', '20-24', '25-30', '31-40', '41-50', '50+'],
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.PIXEL_BODY_STANDARD,
            padding=[Layout.PADDING_SMALL, Layout.SPACING_SMALL],
            size_hint_y=None,
            height=Layout.INPUT_HEIGHT,
            background_color=Colors.BACKGROUND_LIGHT_GRAY
        )
        age_layout.add_widget(age_label)
        age_layout.add_widget(self.age_spinner)
        main_layout.add_widget(age_layout)
        
        # Gender 
        gender_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=Layout.INPUT_HEIGHT + Layout.SUBTITLE_HEIGHT + Layout.SPACING_SMALL,
            spacing=Layout.SPACING_SMALL
        )
        gender_label = self.create_subtitle('Gender:', color=Colors.TEXT_BLACK)
        gender_label.font_name = PixelUI.FONT_BODY
        gender_label.font_size = Typography.PIXEL_BODY_STANDARD
        gender_label.size_hint_y = None
        gender_label.height = Layout.SUBTITLE_HEIGHT
        
        self.gender_spinner = Spinner(
            text='Prefer not to say',
            values=['Male', 'Female', 'Other', 'Prefer not to say'],
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.PIXEL_BODY_STANDARD,
            padding=[Layout.PADDING_SMALL, Layout.SPACING_SMALL],
            size_hint_y=None,
            height=Layout.INPUT_HEIGHT,
            background_color=Colors.BACKGROUND_LIGHT_GRAY
        )
        
        gender_layout.add_widget(gender_label)
        gender_layout.add_widget(self.gender_spinner)
        main_layout.add_widget(gender_layout)
        
        main_layout.add_widget(BoxLayout(size_hint_y=0.1))
        
        
        continue_btn = self.create_button(
            text=Strings.BTN_CONTINUE,
            on_press=self.on_continue,
            button_type='success'
        )
        main_layout.add_widget(continue_btn)
        
        # Set content to pixel frame
        self.pixel_frame.set_content(main_layout)
        self.add_widget(self.pixel_frame)

    def on_enter(self):
        """Refresh participant ID input every time screen is shown (e.g. after reset)."""
        app = App.get_running_app()
        current_id = app.user_data.get('participant_id', '')
        self.id_input.text = current_id

    def on_continue(self, instance):
        """Save data and navigate to Instructions"""
        app = App.get_running_app()
        
        # Use whatever is typed in the box; fall back to current app.user_data ID
        typed = self.id_input.text.strip()
        participant_id = typed if typed else app.user_data.get('participant_id', '')
        
        # Store demographics data
        app.user_data['participant_id'] = participant_id
        app.user_data['demographics'] = {
            'age_range': self.age_spinner.text,
            'gender': self.gender_spinner.text
        }
        
        print(f"Demographics SAVED: {app.user_data}")
        self.manager.current = 'instructions'
