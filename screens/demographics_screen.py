
# screens/demographics_screen.py 
"""
Demographics Screen: Optional participant info
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.app import App

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings
from screens.utils import get_or_create_participant_id


class DemographicsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(DemographicsScreen, self).__init__(**kwargs)
        
        main_layout = BoxLayout(
            orientation='vertical',
            padding=Layout.PADDING_STANDARD,
            spacing=Layout.SPACING_STANDARD
        )
        
        header = self.create_header_bar(show_quit=True, show_reset=False)
        main_layout.add_widget(header)
 
        title_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=Layout.TITLE_HEIGHT + Layout.SUBTITLE_HEIGHT,
            spacing=Layout.SPACING_TINY
        )
        
        title = self.create_title('Participant Information', size='standard')
        subtitle = self.create_subtitle('(All fields optional)')
        
        title_layout.add_widget(title)
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
        id_label.font_size = Typography.BODY_STANDARD
        id_label.size_hint_y = None
        id_label.height = Layout.SUBTITLE_HEIGHT
        
        # Get or create participant ID
        participant_id, is_new = get_or_create_participant_id()
        
        self.id_input = self.create_input_field(
            hint_text='Auto-generated (or enter custom ID)',
            multiline=False
        )
        self.id_input.text = participant_id  # Pre-fill with participant ID
        
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
        age_label.font_size = Typography.BODY_STANDARD
        age_label.size_hint_y = None
        age_label.height = Layout.SUBTITLE_HEIGHT
        
        self.age_spinner = Spinner(
            text='Select Age Range',
            values=['15-19', '20-24', '25-30', '31-40', '41-50', '50+'],
            font_size=Typography.BODY_STANDARD,
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
        gender_label.font_size = Typography.BODY_STANDARD
        gender_label.size_hint_y = None
        gender_label.height = Layout.SUBTITLE_HEIGHT
        
        self.gender_spinner = Spinner(
            text='Prefer not to say',
            values=['Male', 'Female', 'Other', 'Prefer not to say'],
            font_size=Typography.BODY_STANDARD,
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
        
        self.add_widget(main_layout)
    
    def on_continue(self, instance):
        """Save data and navigate to Instructions"""
        app = App.get_running_app()
        
        # Get participant ID (use entered text or keep auto-generated)
        participant_id = self.id_input.text.strip()
        
        # Store demographics data
        app.user_data['participant_id'] = participant_id
        app.user_data['demographics'] = {
            'age_range': self.age_spinner.text,
            'gender': self.gender_spinner.text
        }
        
        print(f"Demographics SAVED: {app.user_data}")
        self.manager.current = 'instructions'
