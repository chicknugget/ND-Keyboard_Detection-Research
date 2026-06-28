# screens/completion_screen.py 

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.widget import Widget

from screens.base_screen import BaseScreen
from screens.config import Colors, Layout, Typography, Strings, PixelUI, BASE_PATH
from screens.utils import load_participant_data
import os

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.image import Image as KivyImage
from kivy.clock import Clock


class CompletionScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(CompletionScreen, self).__init__(enable_wrapper=True,
                                                title='THANK YOU! ',
                                                show_stars=True,
                                                show_header=True,
                                                show_quit=False,
                                                show_reset=False, **kwargs)
        # Override title bar to be taller on completion screen only
        if hasattr(self, 'title_bar') and self.title_bar:
            self.title_bar.size_hint_y = 0.12   # increase from 0.09 to 0.14
    
        
        # Add mushroom handsdown below title (in the main container)
        self._add_mushroom_below_title()
        
        # Main content layout (preserved structure)
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(8), dp(6), dp(8), dp(8)],
            spacing=dp(8)
        )
        
        # Completion confirmation
        self.complete_msg = Label(
            text='You completed all 7 games successfully!',
            color=Colors.TEXT_BLACK,
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.PIXEL_BODY_STANDARD,
            bold=True,
            halign='center',
            valign='middle',
            size_hint_y=0.12
        )
        self.complete_msg.bind(
            size=lambda i, v: setattr(i, 'text_size', (v[0], v[1]))
        )

        main_layout.add_widget(self.complete_msg)
        
        # Session Summary Box
        # Session Summary Box — scrollable so stats text never overflows
        summary_scroll_content = BoxLayout(
            orientation='vertical', size_hint_y=None, padding=[dp(6), dp(6), dp(6), dp(6)], spacing=dp(6)
        )
        summary_scroll_content.bind(minimum_height=summary_scroll_content.setter('height'))

        summary_title = Label(
            text='Session Summary',
            font_name=PixelUI.FONT_TITLE,
            font_size=Typography.PIXEL_TITLE_SMALL,
            color=Colors.PIXEL_BG_GREEN,
            bold=True,
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(36)
        )
        summary_title.bind(size=summary_title.setter('text_size'))

        self.stats_label = Label(
            text='Loading stats...',
            color=Colors.TEXT_BLACK,
            font_name=PixelUI.FONT_BODY,
            font_size=Typography.PIXEL_BODY_STANDARD,
            halign='left',
            valign='top',
            size_hint_y=None,
            size_hint_x=1
        )
        self.stats_label.bind(
            width=lambda i, v: setattr(i, 'text_size', (max(v - dp(8), 0), None)),
            texture_size=lambda i, v: setattr(i, 'height', v[1])
        )
        summary_scroll_content.add_widget(summary_title)
        summary_scroll_content.add_widget(self.stats_label)

        summary_container = self.create_scrollable_content(summary_scroll_content, size_hint=(1, 1))
        main_layout.add_widget(summary_container)
                

        # Buttons: ONLY Replay and Close
        buttons_layout = BoxLayout(
            orientation='horizontal',
            # size_hint_y=None,
            # height=Layout.BUTTON_HEIGHT_STANDARD + Layout.SPACING_STANDARD,
            size_hint_y= 0.12,
            spacing=Layout.SPACING_STANDARD,
            padding=(dp(2), 0)
        )
        
        # REPLAY button 
        replay_btn = self.create_button(
            text=Strings.BTN_REPLAY,
            on_press=self.on_replay,
            button_type='success'
        )
        replay_btn.size_hint_x = 0.5
        replay_btn.size_hint_y=1
        replay_btn.bind(height=lambda inst, val: setattr(inst, 'font_size',val*0.35))
        buttons_layout.add_widget(replay_btn)
        
        # CLOSE APP button
        close_btn = self.create_button(
            text=Strings.BTN_CLOSE,
            on_press=self.on_close,
            button_type='danger'
        )
        close_btn.size_hint_x = 0.5
        close_btn.background_color = Colors.DANGER_RED_DARK
        close_btn.size_hint_y=1
        close_btn.bind(height=lambda inst, val: setattr(inst, 'font_size',val*0.35))
        
        buttons_layout.add_widget(close_btn)
        
        main_layout.add_widget(buttons_layout)
        
        self.set_content(main_layout)


    def _add_mushroom_below_title(self):
        """Add mushroom handsdown image below the title, resizes with window"""
        source = os.path.join(BASE_PATH, 'assets', 'ui', 'mushroom_handsdown.png')
        if not os.path.exists(source):
            return

        mushroom_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.25,       # proportional — 25% of main_container height
            spacing=dp(10),
            padding=[dp(20), dp(5)]
        )

        mush_img = Image(
            source=source,
            size_hint=(None, None),
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={'center_x': 0.5}
        )
        # Bind BOTH dimensions to the parent row's height so it scales with window
        def resize_mushroom(row, val):
            mush_img.height = val * 0.95
            mush_img.width = val * 0.95

        mushroom_row.bind(height=resize_mushroom)

        mushroom_row.add_widget(Widget())    # Left spacer — pushes image to center
        mushroom_row.add_widget(mush_img)
        mushroom_row.add_widget(Widget())    # Right spacer

        if hasattr(self, 'main_container'):
            self.main_container.add_widget(mushroom_row, index=1)
    
    def on_enter(self):
        """Update stats when screen is entered"""
        super().on_enter()
        
        # Get dynamic stats from session
        app = App.get_running_app()

        user_data = app.user_data if hasattr(app,'user_data') else {}

        games_completed = len(app.user_data.get('tasks', []))
        
        tasks = app.user_data.get('tasks', [])
        total_keystrokes = sum(len(t.get('typed_text', '')) for t in tasks)

        # Get total sessions from persistent storage
        participant_data = load_participant_data()
        total_sessions = participant_data.get('total_sessions', 1)
        participant_id = app.user_data.get('participant_id', 'Unknown')
        
        # Calculate session time if available
        session_start = app.user_data.get('session_start_time', '')
        session_end = app.user_data.get('session_end_time', '')

        if session_start and session_end:
            duration_ms = session_end - session_start
            minutes = int(duration_ms / 60000)
            session_time = f"{minutes} minutes"
        else:
            session_time = "5 minutes"
                
        # UI text
        if games_completed == 7:
            self.complete_msg.text = 'CONGRATULATIONS! \nYou completed all 7 levels successfully'
        elif games_completed > 0:
            self.complete_msg.text = f'You completed {games_completed} levels out of 7 levels.'
        else:
            self.complete_msg.text = 'Session ended. \nNo levels completed.'
        
        # Update stats text
        stats_text = (
            f"- Participant ID:\n  {participant_id}\n"
            f"- {games_completed} levels completed\n"
            f"- {session_time} total time\n"
            f"- Total sessions: {total_sessions}\n\n"
            "Thank you for being a part of our study.\nWe truly appreciate the time and effort you've shared with us.\nYour participation means a lot to our team."
        )
        
        self.stats_label.text = stats_text
        
        print(f" Completion screen showing: {games_completed} levels, {total_keystrokes} keystrokes")

        # Show congratulations popup if user naturally completed all 7 levels
        if games_completed == 7 : #and 'session_end_time' not in app.user_data:
            # Clock.schedule_once(lambda dt: self._show_congrats_popup(), 0.3)
            Clock.schedule_once(lambda dt: self._show_congrats_popup(), 0.1)
    



    def _show_congrats_popup(self):
        """Show congratulations overlay popup for completing all 7 levels"""

        overlay = FloatLayout()

        # Dark semi-transparent background
        with overlay.canvas.before:
            Color(0, 0, 0, 0.50)
            overlay.bg_rect = RoundedRectangle(pos=overlay.pos, size=overlay.size, radius=[dp(20)])
        overlay.bind(
            pos=lambda i, v: setattr(i.bg_rect, 'pos', v),
            size=lambda i, v: setattr(i.bg_rect, 'size', v)
        )

        # Content box centered in the overlay
        content_box = BoxLayout(
            orientation='vertical',
            size_hint=(0.95, 0.95),
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            spacing=dp(14),
            padding=dp(16)
        )

        # White rounded card background
        with content_box.canvas.before:
            Color(212/255, 177/255, 66/255, 1)
            content_box.card_rect = RoundedRectangle(
                pos=content_box.pos, size=content_box.size, radius=[dp(24)]
            )
        content_box.bind(
            pos=lambda i, v: setattr(i.card_rect, 'pos', v),
            size=lambda i, v: setattr(i.card_rect, 'size', v)
        )

        # Congratulations image
        congrats_img_path = os.path.join(BASE_PATH, 'assets', 'ui', 'congratulations.png')
        if os.path.exists(congrats_img_path):
            img = KivyImage(
                source=congrats_img_path,
                size_hint=(1, 0.85),
                allow_stretch=True,
                keep_ratio=True
            )
        else:
            # Fallback: text label if no image asset
            img = Label(
                text='\nCONGRATULATIONS!',
                font_size=dp(28),
                color=Colors.SUCCESS_GREEN,
                halign='center',
                valign='middle',
                bold=True,
                size_hint=(1, 0.80)
            )
            img.bind(size=img.setter('text_size'))

        content_box.add_widget(img)

        # YEAH button — green, rounded
        popup_ref = [None]  # mutable reference so inner func can access popup

        yeah_btn = Button(
            text='YEAH!',
            size_hint=(0.65, None),
            font_name=PixelUI.FONT_TITLE,
            height=dp(45),
            pos_hint={'center_x': 0.5},
            background_normal='',
            # background_color=Colors.PIXEL_BG_GREEN,
            background_color=(0,0,0,0), #transparent
            color=(0.95, 0.95, 0.90, 1),
            bold=True,
            font_size=dp(18)
        )

        # Rounded corners on the YEAH button via canvas
        with yeah_btn.canvas.before:
            Color(*Colors.PIXEL_BG_GREEN)
            yeah_btn.btn_rect = RoundedRectangle(
                pos=yeah_btn.pos,
                size=yeah_btn.size,
                radius=[dp(24)]
            )
        yeah_btn.bind(
            pos=lambda i, v: setattr(i.btn_rect, 'pos', v),
            size=lambda i, v: setattr(i.btn_rect, 'size', v)
        )

        def on_yeah(instance):
            if popup_ref[0]:
                popup_ref[0].dismiss()

        yeah_btn.bind(on_press=on_yeah)
        content_box.add_widget(yeah_btn)
        overlay.add_widget(content_box)

        popup = Popup(
            content=overlay,
            size_hint=(1, 1),           # full screen
            background='',              # no default Popup chrome
            background_color=(0, 0, 0, 0),  # transparent — our overlay draws its own bg
            separator_height=0,
            title='',
            auto_dismiss=False
        )
        popup_ref[0] = popup
        popup.open()



    # def on_replay(self, instance):
    #     """Replay game - skip to instructions with new session ID"""
    #     app = App.get_running_app()

    #     participant_id = app.user_data.get('participant_id')
    #     demographics = app.user_data.get('demographics', {})
        
    #     # Generate new session ID
    #     # session_id = generate_session_id() //redundant
        
    #     # Reset user data
    #     app.user_data = {
    #         'participant_id': participant_id,
    #         'demographics': demographics,
    #         'session_id': None, #session_id,
    #         'current_game': 0,
    #         'tasks': [],
    #         'debriefing_complete': False
    #     }
        
    #     print(f" REPLAY pressed")
    #     self.manager.current = 'instructions'
    
    # def on_close(self, instance):
    #     """Close the entire app"""
    #     print("Session closed")
    #     App.get_running_app().stop()


    def on_replay(self, instance):

        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        content.add_widget(Label(
            text='You want to play again',
            color=Colors.TEXT_BLACK, halign='center', valign='middle'
        ))
        content.children[0].bind(size=content.children[0].setter('text_size'))
        btn_row = BoxLayout(spacing=dp(10), size_hint_y=0.4)
        popup = Popup(title='Replay Session', content=content,
                    size_hint=(0.7, 0.35), auto_dismiss=False)

        def do_replay(*_):
            popup.dismiss()
            app = App.get_running_app()
            participant_id = app.user_data.get('participant_id')
            demographics = app.user_data.get('demographics', {})
            app.user_data = {
                'participant_id': participant_id,
                'demographics': demographics,
                'session_id': None,
                'current_game': 0,
                'tasks': [],
                'debriefing_complete': False
            }
            print(" REPLAY pressed")
            self.manager.current = 'instructions'

        btn_row.add_widget(Button(text='Yes, Replay', on_press=do_replay))
        btn_row.add_widget(Button(text='Cancel', on_press=lambda *_: popup.dismiss()))
        content.add_widget(btn_row)
        popup.open()


    def on_close(self, instance):

        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        content.add_widget(Label(
            text='Are you sure you want to close the app?',
            color=Colors.TEXT_BLACK, halign='center', valign='middle'
        ))
        content.children[0].bind(size=content.children[0].setter('text_size'))
        btn_row = BoxLayout(spacing=dp(10), size_hint_y=0.4)
        popup = Popup(title='Close App', content=content,
                    size_hint=(0.7, 0.35), auto_dismiss=False)
        btn_row.add_widget(Button(text='Yes, Close',
                                on_press=lambda *_: App.get_running_app().stop()))
        btn_row.add_widget(Button(text='Cancel',
                                on_press=lambda *_: popup.dismiss()))
        content.add_widget(btn_row)
        popup.open()

        
