# screens/demographics_screen.py 

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.app import App
from kivy.metrics import dp

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings, PixelUI
from screens.utils import load_participant_data  # kept for potential future use

from screens.config import SoundManager


class DemographicsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(DemographicsScreen, self).__init__(
                enable_wrapper=True,
                title='Participant Information',
                show_stars=True,
                show_header=True,
                show_quit=True,
                show_reset=False,**kwargs)
        
        
        # Original main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=Layout.PADDING_STANDARD,
            spacing=Layout.SPACING_STANDARD
        )
 
        title_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.14,
            spacing=Layout.SPACING_TINY
        )

        info_label = self.create_subtitle('Please provide the details below', color=Colors.TEXT_BLACK)
        info_label.font_name = PixelUI.FONT_BODY
        info_label.font_size = Typography.PIXEL_BODY_STANDARD
        info_label.bold =True
        info_label.size_hint_y = 0.14

        subtitle = self.create_subtitle('(All fields optional)')
        subtitle.font_name = PixelUI.FONT_BODY
        subtitle.font_size = Typography.PIXEL_BODY_SMALL
        subtitle.size_hint_y = 0.10

        title_layout.add_widget(info_label)
        title_layout.add_widget(subtitle)
        main_layout.add_widget(title_layout)

        
        # Participant ID - Auto-generated but editable
        id_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.16,
            spacing=Layout.SPACING_SMALL
        )
        id_label = self.create_subtitle('Participant ID:', color=Colors.TEXT_BLACK)
        id_label.font_name = PixelUI.FONT_BODY
        id_label.font_size = Typography.PIXEL_BODY_STANDARD
        id_label.bold = True
        id_label.size_hint_y = 0.5
        # id_label.height=None
        
        self.id_input = self.create_input_field(
            hint_text='Auto-generated',
            multiline=False
        )
        self.id_input.font_name = PixelUI.FONT_BODY
        self.id_input.readonly= True
        self.id_input.disabled = False
        self.id_input.size_hint_y = 0.5
        self.id_input.background_color =(0.95, 0.93, 0.88, 1)
        self.id_input.foreground_color = Colors.TEXT_BLACK
        self.id_input.padding = [Layout.PADDING_SMALL, Layout.SPACING_SMALL]
        self.id_input.bind(height=lambda inst, val : setattr(inst, 'font_size', max(val*0.38,10)))
        # (0.95, 0.93, 0.88, 1) beige
        # (0.88, 0.85, 0.95, 1) lavender

        # Text will be populated in on_enter so it always reflects the current participant ID 

        id_layout.add_widget(id_label)
        id_layout.add_widget(self.id_input)
        main_layout.add_widget(id_layout)
        
        # Age Range
        age_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.16,
            spacing=Layout.SPACING_SMALL
        )  
        age_label = self.create_subtitle('Age Range:', color=Colors.TEXT_BLACK)
        age_label.font_name = PixelUI.FONT_BODY
        # age_label.size_hint_y =0.15
        age_label.font_size = Typography.PIXEL_BODY_STANDARD
        age_label.bold=True 
        age_label.size_hint_y = 0.5

        self.age_spinner = Spinner(
            text='Select Age Range',
            values=['15-19', '20-24', '25-30', '31-40', '41-50', '50+'],
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.PIXEL_BODY_STANDARD,
            padding=[Layout.PADDING_SMALL, Layout.SPACING_SMALL],
            size_hint_y=0.6,
            background_normal='',
            background_color=(0.95, 0.93, 0.88, 1),
            color=Colors.TEXT_BLACK
        )
        self.age_spinner.bind(height=lambda inst, val: setattr(inst, 'font_size', max(val * 0.35, 10)))
        self.age_spinner.bind(on_press=lambda inst: SoundManager.play('tick'))
        self.age_spinner.bind(text=lambda inst, val: SoundManager.play('tick'))
        age_layout.add_widget(age_label)
        age_layout.add_widget(self.age_spinner)
        main_layout.add_widget(age_layout)
        
        # Gender 
        gender_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.16,
            spacing=Layout.SPACING_SMALL
        )
        gender_label = self.create_subtitle('Gender:', color=Colors.TEXT_BLACK)
        gender_label.font_name = PixelUI.FONT_BODY
        # gender_label.size_hint_y = 0.15
        gender_label.font_size = Typography.PIXEL_BODY_STANDARD
        gender_label.bold = True
        gender_label.size_hint_y = 0.5
        
        self.gender_spinner = Spinner(
            text='Select Gender',
            values=['Male', 'Female', 'Other', 'Prefer not to say'],
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.PIXEL_BODY_STANDARD,
            padding=[Layout.PADDING_SMALL, Layout.SPACING_SMALL],
            size_hint_y=0.6,
            background_normal='',
            background_color=(0.95, 0.93, 0.88, 1),
            color=Colors.TEXT_BLACK
        )
        self.gender_spinner.bind(height=lambda inst, val: setattr(inst, 'font_size', max(val * 0.35, 10)))
        self.gender_spinner.bind(on_press=lambda inst: SoundManager.play('tick'))
        self.gender_spinner.bind(text=lambda inst, val: SoundManager.play('tick'))
        
        gender_layout.add_widget(gender_label)
        gender_layout.add_widget(self.gender_spinner)
        main_layout.add_widget(gender_layout)
        
        main_layout.add_widget(BoxLayout(size_hint_y=0.1))
        
        
        continue_btn = self.create_button(
            text=Strings.BTN_CONTINUE,
            on_press=self.on_continue,
            button_type='success'
        )
        continue_btn.size_hint_y =0.10
        main_layout.add_widget(continue_btn)
        
        # Set content to main layout
        self.set_content(main_layout)

    def on_enter(self):
        """Refresh all fields every time screen is shown (e.g. after reset)."""
        super().on_enter() if hasattr(super(), 'on_enter') else None
        app = App.get_running_app()
        current_id = app.user_data.get('participant_id', '')
        self.id_input.text = current_id
        self.age_spinner.text = 'Select Age Range'
        self.gender_spinner.text = 'Select Gender'



    def on_continue(self, instance):
        """Save data and navigate to Instructions"""

        SoundManager.play('positive')

        app = App.get_running_app()
        
        participant_id=app.user_data.get('participant_id','')
        
        # Store demographics data
        app.user_data['participant_id'] = participant_id
        age = self.age_spinner.text if self.age_spinner.text != 'Select Age Range' else 'Not selected'
        app.user_data['demographics'] = {
            'age_range': age,
            'gender': self.gender_spinner.text
        }

        
        print(f"Demographics SAVED: {app.user_data}")
        self.manager.current = 'instructions'
