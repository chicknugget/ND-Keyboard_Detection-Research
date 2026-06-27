# screens/consent_screen.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.app import App
from kivy.properties import ListProperty
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings, PixelUI
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button

class ConsentScreen(BaseScreen):
    # all_checkboxes = ListProperty()


    def __init__(self, **kwargs):
        super(ConsentScreen, self).__init__(enable_wrapper=True, title='INFORMED CONSENT', show_stars=True, show_header=True, show_quit=False, show_reset=False, **kwargs)
        
       
        
        # Original main layout (preserved exactly)
        main_layout = BoxLayout(
            orientation='vertical',
            padding=Layout.PADDING_STANDARD,
            spacing=Layout.SPACING_STANDARD
        )
        
        # Scrollable info section
        info_text = """
Welcome!

Thank you for taking the time to participate in our study on emotion
recognition through typing patterns. Your contribution will help us better
understand how emotions may influence the way people type.

ABOUT THIS STUDY:
 -We are exploring how emotions affect typing patterns (keystroke dynamics)
 -This is an academic research project
 -Participation takes approximately 5–10 minutes

YOUR PRIVACY:
 -We collect only typing timing and keystroke patterns
 -No personal information is collected
 -Your data will be stored securely and used only for research purposes

WHAT TO EXPECT:
 -Some tasks may be slightly challenging and could cause mild, temporary frustration
 -Your participation is completely voluntary
 -You may withdraw from the study at any time before submitting your data

By checking all of the boxes below, you confirm that:
 -You are 18+ years of age or older
 -You have read and understood the study information
 -You understand what participation involves
 -You voluntarily agree to take part in this study
"""
        
        info_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=Layout.PADDING_CARD,
            spacing=Layout.SPACING_SMALL
        )
        info_layout.bind(minimum_height=info_layout.setter('height'))
        
        info_label = Label(
        text=info_text,
        font_name=PixelUI.FONT_BODY,
        # Remove font_size from here
        color=Colors.TEXT_BLACK,
        halign='left',
        valign='top',
        size_hint_y=None,
        markup=True
        )
        self.bind(height=lambda inst, val: setattr(info_label, 'font_size', val * 0.02))
            

        # def set_text_size(instance, value):
        #     # instance.text_size = (value - Layout.PADDING_CARD * 2, None)
        #     instance.text_size = (value , None)
        
        info_label.bind(width=lambda inst, val: setattr(inst, 'text_size', (val, None)))
        info_label.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
        info_layout.add_widget(info_label)
        
        # scrollable card for info
        scroll_card = self.create_scrollable_content(info_layout,size_hint=(1,0.45))
        main_layout.add_widget(scroll_card)

        # Checkboxes 
        checkboxes_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.25,
            spacing=Layout.SPACING_SMALL + Layout.SPACING_TINY
        )
        # checkboxes_layout.bind(minimum_height=checkboxes_layout.setter('height'))
        
        checkbox_texts = [
    'I have read and understood the study information and I\'m 18+',
    'I understand that some tasks may cause mild, temporary frustration',
    'I voluntarily agree to participate in this study'
]
        
        self.all_checkboxes = []
        for text in checkbox_texts:
            cb_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=1/3,
                # height=Layout.BUTTON_HEIGHT_TINY,
                spacing=Layout.SPACING_SMALL,
                padding=[dp(6), dp(2), dp(6), dp(2)]

            )
            with cb_layout.canvas.before:
                Color(254 / 255, 240 / 255, 225 / 255, 0.55)  # #FEF0E1 strip
                cb_row_bg = RoundedRectangle(radius=[dp(5)])
            cb_layout.bind(
                pos=lambda i, v, r=cb_row_bg: setattr(r, 'pos', i.pos),
                size=lambda i, v, r=cb_row_bg: setattr(r, 'size', i.size)
            )
            
            checkbox = CheckBox(
                size_hint=(None, 0.8),
                size=(Layout.CHECKBOX_SIZE + 6, Layout.CHECKBOX_SIZE + 6),
                active=False,
                color=Colors.PRIMARY_BLUE_DARK  
            )
            checkbox.bind(height=lambda inst, val: setattr(inst, 'width', val))
            
            # Label(Text shown) for checkbox
            cb_label = Label(
                text=text,
                font_name=PixelUI.FONT_BODY,
                # font_size=Typography.PIXEL_BODY_SMALL,
                color=Colors.TEXT_BLACK,  
                halign='left',
                valign='middle',
                size_hint_x=1
            )
            
            cb_label.bind(
                size=cb_label.setter('text_size')  # Wrap text to widget width
            )
            cb_label.bind(height=lambda inst, val: setattr(inst, 'font_size', val * 0.42))

            cb_layout.add_widget(checkbox)
            cb_layout.add_widget(cb_label)
            checkboxes_layout.add_widget(cb_layout)
            
            self.all_checkboxes.append(checkbox)
            checkbox.bind(active=self.update_consent_button)
        
        main_layout.add_widget(checkboxes_layout)
        
        
        buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.09,
            # height=Layout.BUTTON_HEIGHT_LARGE,
            spacing=Layout.SPACING_LARGE
        )
        
        # Decline button
        decline_btn = self.create_button(
            text=Strings.BTN_DECLINE,
            on_press=self.on_decline,
            button_type='danger'
        )
        decline_btn.size_hint_x = 0.48
        decline_btn.size_hint_y=1 #fill parent height
        buttons_layout.add_widget(decline_btn)
        
        # Consent button (initially disabled)
        self.consent_btn = self.create_button(
            text=Strings.BTN_CONSENT,
            on_press=self.on_consent,
            button_type='success',
            disabled=True
        )
        self.consent_btn.size_hint_x = 0.48
        self.consent_btn.size_hint_y=1 #fill parent height
        self.consent_btn.background_color = Colors.DISABLED_GRAY  
        buttons_layout.add_widget(self.consent_btn)

        main_layout.add_widget(buttons_layout)
        
        # Set content to main layout
        self.set_content(main_layout)


    def update_consent_button(self, instance, value):
        """Enable CONSENT button only when ALL 3 checkboxes checked"""
        all_checked = all(cb.active for cb in self.all_checkboxes)
        self.consent_btn.disabled = not all_checked

        if all_checked:
            self.consent_btn.background_color = Colors.SUCCESS_GREEN
        else:
            self.consent_btn.background_color = Colors.DISABLED_GRAY

    #to reset checkboxes
    def reset_consent(self):
        """Reset all checkboxes to unchecked and disable consent button"""
        for cb in self.all_checkboxes:
            cb.active = False
        self.consent_btn.disabled = True
        self.consent_btn.background_color = Colors.DISABLED_GRAY

    def on_pre_enter(self, *args):
        """Reset checkboxes every time screen is entered"""
        super().on_pre_enter(*args)
        self.reset_consent()



    def on_consent(self, instance):
        """Go to next screen (Demographics)"""
        print("CONSENT GIVEN - Going to Demographics")
        self.manager.current = 'demographics'

    
    # def on_decline(self, instance):
    #     """Close app when declined"""
    #     print("Study declined - Closing app")
    #     App.get_running_app().stop()

    def on_decline(self, instance):
    
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        content.add_widget(Label(
            text='Are you sure you want to decline?\nThe app will close.',
            color=Colors.TEXT_BLACK, halign='center', valign='middle'
        ))
        
        btn_row = BoxLayout(spacing=dp(10), size_hint_y=0.4)
        popup = Popup(title='Confirm Decline', content=content, size_hint=(0.8, 0.35), auto_dismiss=False)
        
        btn_row.add_widget(Button(text='Yes, Decline', on_press=lambda *_: App.get_running_app().stop()))
        btn_row.add_widget(Button(text='Go Back', on_press=lambda *_: popup.dismiss()))
        content.add_widget(btn_row)
        
        popup.open()

