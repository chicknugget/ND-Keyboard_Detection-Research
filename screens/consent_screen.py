# screens/consent_screen.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.app import App
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings, PixelUI
from screens.pixel_ui_wrapper import PixelFrame


class ConsentScreen(BaseScreen):
    all_checkboxes = ListProperty()

    def __init__(self, **kwargs):
        super(ConsentScreen, self).__init__(**kwargs)
        
        # Create pixel frame wrapper
        self.pixel_frame = PixelFrame(
            title='INFORMED CONSENT',
            show_stars=True,
            show_header=True,
            show_quit=False,
            show_reset=False
        )
        
        # Original main layout (preserved exactly)
        main_layout = BoxLayout(
            orientation='vertical',
            padding=Layout.PADDING_STANDARD,
            spacing=Layout.SPACING_STANDARD
        )
        
        # Scrollable info section
        info_text = """
Welcome to our emotion recognition study through typing patterns.

WHAT WE'RE STUDYING:
• How emotions affect keystroke dynamics  
• Anonymous data collection only
• Academic research (no commercial use)
• Takes 5-10 minutes total

YOUR DATA:
• Keystroke timing + patterns only
• No personal information collected
• Stored securely, used for publication
• You can withdraw anytime

By checking all boxes below, you confirm:
• You are 18+ years old
• You understand the study purpose
• You voluntarily agree to participate
        """
        
        info_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=Layout.PADDING_CARD,
            spacing=Layout.SPACING_SMALL
        )
        info_layout.bind(minimum_height=info_layout.setter('height'))
        
        from kivy.uix.label import Label
        info_label = Label(
            text=info_text,
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.PIXEL_BODY_SMALL,
            color=Colors.TEXT_BLACK,  
            halign='left',
            valign='top',
            size_hint_y=None,
            markup=True
        )
        

        def set_text_size(instance, value):
            instance.text_size = (value - Layout.PADDING_CARD * 2, None)
        
        info_label.bind(
            width=set_text_size,
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        info_layout.add_widget(info_label)
        
        # scrollable card for info
        scroll_card = self.create_scrollable_content(info_layout)
        main_layout.add_widget(scroll_card)

        # Checkboxes 
        checkboxes_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=Layout.SPACING_SMALL + Layout.SPACING_TINY
        )
        checkboxes_layout.bind(minimum_height=checkboxes_layout.setter('height'))
        
        checkbox_texts = [
            'I have read and understand the study information',
            'I understand this study may induce frustration',
            'I voluntarily agree to participate'
        ]
        
        self.all_checkboxes = []
        for text in checkbox_texts:
            cb_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=Layout.BUTTON_HEIGHT_TINY,
                spacing=Layout.SPACING_SMALL
            )
            
            checkbox = CheckBox(
                size_hint=(None, None),
                size=(Layout.CHECKBOX_SIZE + 6, Layout.CHECKBOX_SIZE + 6),
                active=False,
                color=Colors.PRIMARY_BLUE_DARK  
            )
            
            # Label for checkbox
            from kivy.uix.label import Label
            cb_label = Label(
                text=text,
                font_name=PixelUI.FONT_BODY,
                font_size=Typography.PIXEL_BODY_SMALL,
                color=Colors.TEXT_BLACK,  
                halign='left',
                valign='middle',
                size_hint_x=1
            )
            
            cb_label.bind(
                width=lambda instance, value: setattr(instance, 'text_size', (value, None)),
                texture_size=lambda instance, value: setattr(cb_layout, 'height', max(
                    Layout.BUTTON_HEIGHT_TINY, value[1] + Layout.SPACING_SMALL
                ))
            )

            cb_layout.add_widget(checkbox)
            cb_layout.add_widget(cb_label)
            checkboxes_layout.add_widget(cb_layout)
            
            self.all_checkboxes.append(checkbox)
            checkbox.bind(active=self.update_consent_button)
        
        main_layout.add_widget(checkboxes_layout)
        
        
        buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=Layout.BUTTON_HEIGHT_LARGE,
            spacing=Layout.SPACING_LARGE
        )
        
        # Decline button
        decline_btn = self.create_button(
            text=Strings.BTN_DECLINE,
            on_press=self.on_decline,
            button_type='danger'
        )
        decline_btn.size_hint_x = 0.48
        buttons_layout.add_widget(decline_btn)
        
        # Consent button (initially disabled)
        self.consent_btn = self.create_button(
            text=Strings.BTN_CONSENT,
            on_press=self.on_consent,
            button_type='success',
            disabled=True
        )
        self.consent_btn.size_hint_x = 0.48
        self.consent_btn.background_color = Colors.DISABLED_GRAY  
        buttons_layout.add_widget(self.consent_btn)

        main_layout.add_widget(buttons_layout)
        
        # Set content to pixel frame
        self.pixel_frame.set_content(main_layout)
        self.add_widget(self.pixel_frame)

    def update_consent_button(self, instance, value):
        """Enable CONSENT button only when ALL 3 checkboxes checked"""
        all_checked = all(cb.active for cb in self.all_checkboxes)
        self.consent_btn.disabled = not all_checked

        if all_checked:
            self.consent_btn.background_color = Colors.SUCCESS_GREEN
        else:
            self.consent_btn.background_color = Colors.DISABLED_GRAY

    def on_consent(self, instance):
        """Go to next screen (Demographics)"""
        print("CONSENT GIVEN - Going to Demographics")
        self.manager.current = 'demographics'

    def on_decline(self, instance):
        """Close app when declined"""
        print("Study declined - Closing app")
        App.get_running_app().stop()
# # screens/consent_screen.py

# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.checkbox import CheckBox
# from kivy.app import App
# from kivy.properties import ListProperty
# from kivy.core.window import Window

# from screens.base_screen import BaseScreen
# from screens.config import Colors, Layout, Typography, AppConfig, Strings


# class ConsentScreen(BaseScreen):
#     all_checkboxes = ListProperty()

#     def __init__(self, **kwargs):
#         super(ConsentScreen, self).__init__(**kwargs)
         
#         main_layout = BoxLayout(
#             orientation='vertical',
#             padding=Layout.PADDING_LARGE,
#             spacing=Layout.SPACING_STANDARD
#         )
        
#         # Title 
#         title = self.create_title('INFORMED CONSENT')
#         main_layout.add_widget(title)
        
#         # Scrollable info section
#         info_text = """
# Welcome to our emotion recognition study through typing patterns.

# WHAT WE'RE STUDYING:
# • How emotions affect keystroke dynamics  
# • Anonymous data collection only
# • Academic research (no commercial use)
# • Takes 5-10 minutes total

# YOUR DATA:
# • Keystroke timing + patterns only
# • No personal information collected
# • Stored securely, used for publication
# • You can withdraw anytime

# By checking all boxes below, you confirm:
# • You are 18+ years old
# • You understand the study purpose
# • You voluntarily agree to participate
#         """
        
#         info_layout = BoxLayout(
#             orientation='vertical',
#             size_hint_y=None,
#             padding=Layout.PADDING_CARD,
#             spacing=Layout.SPACING_SMALL
#         )
#         info_layout.bind(minimum_height=info_layout.setter('height'))
        
#         from kivy.uix.label import Label
#         info_label = Label(
#             text=info_text,
#             font_size=Typography.BODY_SMALL,
#             color=Colors.TEXT_BLACK,  
#             halign='left',
#             valign='top',
#             size_hint_y=None,
#             markup=True
#         )
        

#         def set_text_size(instance, value):
#             instance.text_size = (value - Layout.PADDING_CARD * 2, None)
        
#         info_label.bind(
#             width=set_text_size,
#             texture_size=lambda instance, value: setattr(instance, 'height', value[1])
#         )
#         info_layout.add_widget(info_label)
        
#         # scrollable card for info
#         scroll_card = self.create_scrollable_content(info_layout)
#         main_layout.add_widget(scroll_card)

#         # Checkboxes 
#         checkboxes_layout = BoxLayout(
#             orientation='vertical',
#             size_hint_y=None,
#             spacing=Layout.SPACING_SMALL + Layout.SPACING_TINY
#         )
#         checkboxes_layout.bind(minimum_height=checkboxes_layout.setter('height'))
        
#         checkbox_texts = [
#             'I have read and understand the study information',
#             'I understand this study may induce frustration',
#             'I voluntarily agree to participate'
#         ]
        
#         self.all_checkboxes = []
#         for text in checkbox_texts:
#             cb_layout = BoxLayout(
#                 orientation='horizontal',
#                 size_hint_y=None,
#                 height=Layout.BUTTON_HEIGHT_TINY,
#                 spacing=Layout.SPACING_SMALL
#             )
            
#             checkbox = CheckBox(
#                 size_hint=(None, None),
#                 size=(Layout.CHECKBOX_SIZE + 6, Layout.CHECKBOX_SIZE + 6),
#                 active=False,
#                 color=Colors.PRIMARY_BLUE_DARK  
#             )
            
#             # Label for checkbox
#             from kivy.uix.label import Label
#             cb_label = Label(
#                 text=text,
#                 font_size=Typography.BODY_SMALL,
#                 color=Colors.TEXT_BLACK,  
#                 halign='left',
#                 valign='middle',
#                 size_hint_x=1
#             )
            
#             cb_label.bind(
#                 width=lambda instance, value: setattr(instance, 'text_size', (value, None)),
#                 texture_size=lambda instance, value: setattr(cb_layout, 'height', max(
#                     Layout.BUTTON_HEIGHT_TINY, value[1] + Layout.SPACING_SMALL
#                 ))
#             )

#             cb_layout.add_widget(checkbox)
#             cb_layout.add_widget(cb_label)
#             checkboxes_layout.add_widget(cb_layout)
            
#             self.all_checkboxes.append(checkbox)
#             checkbox.bind(active=self.update_consent_button)
        
#         main_layout.add_widget(checkboxes_layout)
        
        
#         buttons_layout = BoxLayout(
#             orientation='horizontal',
#             size_hint_y=None,
#             height=Layout.BUTTON_HEIGHT_LARGE,
#             spacing=Layout.SPACING_LARGE
#         )
        
#         # Decline button
#         decline_btn = self.create_button(
#             text=Strings.BTN_DECLINE,
#             on_press=self.on_decline,
#             button_type='danger'
#         )
#         decline_btn.size_hint_x = 0.48
#         buttons_layout.add_widget(decline_btn)
        
#         # Consent button (initially disabled)
#         self.consent_btn = self.create_button(
#             text=Strings.BTN_CONSENT,
#             on_press=self.on_consent,
#             button_type='success',
#             disabled=True
#         )
#         self.consent_btn.size_hint_x = 0.48
#         self.consent_btn.background_color = Colors.DISABLED_GRAY  
#         buttons_layout.add_widget(self.consent_btn)

#         main_layout.add_widget(buttons_layout)
        
#         self.add_widget(main_layout)

#     def update_consent_button(self, instance, value):
#         """Enable CONSENT button only when ALL 3 checkboxes checked"""
#         all_checked = all(cb.active for cb in self.all_checkboxes)
#         self.consent_btn.disabled = not all_checked

#         if all_checked:
#             self.consent_btn.background_color = Colors.SUCCESS_GREEN
#         else:
#             self.consent_btn.background_color = Colors.DISABLED_GRAY

#     def on_consent(self, instance):
#         """Go to next screen (Demographics)"""
#         print("CONSENT GIVEN - Going to Demographics")
#         self.manager.current = 'demographics'

#     def on_decline(self, instance):
#         """Close app when declined"""
#         print("Study declined - Closing app")
#         App.get_running_app().stop()
