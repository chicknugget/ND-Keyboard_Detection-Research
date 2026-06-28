# screens/base_screen.py 

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty
from kivy.metrics import dp

from screens.config import Colors, Layout, Typography, AppConfig

from kivy.uix.floatlayout import FloatLayout
import os
from screens.config import  BASE_PATH, PixelUI
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.popup import Popup

from screens.config import SoundManager



class BounceButton(Button):
    """Button with built-in bounce animation on press"""
    original_size_x = NumericProperty(0)
    original_size_y = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original_bg_color = None
        self.pressed_color = None
        self.bind(on_press=self._trigger_bounce)
        self.bind(size=self._store_original_size)
        Clock.schedule_once(self._capture_colors, 0)
    def _capture_colors(self, dt):
        self.original_bg_color = self.background_color[:]
        r, g, b, a = self.original_bg_color
        self.pressed_color = (max(0, r * 0.85), max(0, g * 0.85), max(0, b * 0.85), a)
    
    def _store_original_size(self, instance, value):
        if self.original_size_x == 0 and value[0] > 0:
            self.original_size_x = value[0]
            self.original_size_y = value[1]
    
    def _trigger_bounce(self, instance):
        """Trigger bounce animation: scale down to 0.95 then back to 1.0"""
        if self.original_size_x == 0:
            self.original_size_x = self.width
            self.original_size_y = self.height

        # Cancel any existing animation
        Animation.cancel_all(self)
        
        # Create bounce animation: shrink slightly then return to normal
        # Using out_bounce for a nice elastic feel
        target_width = self.original_size_x * 0.95
        target_height = self.original_size_y * 0.95
        
        anim = Animation(
            size=(target_width, target_height), 
            background_color= self.pressed_color,
            duration=0.08, t='out_quad')
        anim += Animation(
            size=(self.original_size_x, self.original_size_y), 
            background_color = self.original_bg_color,
            duration=0.20, t='out_bounce')
        
        anim.start(self)



class PixelTitleBar(BoxLayout):
    title_text = StringProperty('')
    show_stars = True
    visible = True
    
    def __init__(self, title='', show_stars=True, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.09
        self.title_text = title
        self.show_stars = show_stars
        self.padding = [dp(10), dp(5)]
        self.spacing = dp(10)
        self._build()
    
    def _build(self):
        star_path = os.path.join(BASE_PATH, 'assets', 'ui', 'star.png')
        if self.show_stars and os.path.exists(star_path):
            self.left_star = Image(source=star_path, size_hint=(None, None), allow_stretch=True, keep_ratio=True)
            self.bind(height=lambda inst, val: setattr(self.left_star, 'height', val * 0.8))
            self.bind(height=lambda inst, val: setattr(self.left_star, 'width', val * 0.8))
            self.add_widget(self.left_star)
        else:
            self.add_widget(Widget(size_hint_x=0.1))
        
        self.title_label = Label(text=self.title_text, font_name=PixelUI.FONT_TITLE, color=Colors.TEXT_BLACK, halign='center', valign='middle', size_hint_x=1, bold=True)
        self.title_label.bind(size=self.title_label.setter('text_size'))
        self.title_label.bind(height=lambda inst, val: setattr(inst, 'font_size', val * 0.50))
        self.add_widget(self.title_label)
        
        if self.show_stars and os.path.exists(star_path):
            self.right_star = Image(source=star_path, size_hint=(None, None), allow_stretch=True, keep_ratio=True)
            self.bind(height=lambda inst, val: setattr(self.right_star, 'height', val * 0.8))
            self.bind(height=lambda inst, val: setattr(self.right_star, 'width', val * 0.8))
            self.add_widget(self.right_star)
        else:
            self.add_widget(Widget(size_hint_x=0.1))
            
    def set_title(self, text):
        self.title_text = text
        self.title_label.text = text
        
    def slide_up(self, duration=0.3):
        if self.visible:
            target_y = self.parent.height if self.parent else 800
            anim = Animation(y=target_y, duration=duration)
            anim.start(self)
            self.visible = False
            
    def slide_down(self, duration=0.3):
        if not self.visible:
            target_y = (self.parent.height - self.height) if self.parent else 50
            anim = Animation(y=target_y, duration=duration)
            anim.start(self)
            self.visible = True

class BaseScreen(Screen):
    
    def __init__(self, enable_wrapper=False, title='', show_stars=True, 
                 show_decorations=False, decoration_type='handsup', show_header=True, 
                 show_quit=False, show_reset=False, on_reset=None, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.enable_wrapper = enable_wrapper

        if self.enable_wrapper:

            with self.canvas.before:
                #1.setup green mosic image
                mosaic_path = os.path.join(BASE_PATH, 'assets', 'ui', 'green_mosaic.png')
                if os.path.exists(mosaic_path):
                    Color(1,1,1,1)
                    self.bg_rect = Rectangle(
                        source =mosaic_path, size =self.size, pos=self.pos
                    )
                else:
                    Color(0.4,0.7,0.3,1)
                    self.bg_rect= Rectangle(size=self.size, pos=self.pos)

            self.bind(size= self._update_bg, pos= self._update_bg)

            #2.main layout container
            self.main_container = BoxLayout(
                orientation='vertical',
                size_hint=(0.965, 0.965),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                spacing=dp(6)
            )
            #3. setup header bar
            if show_header:
                self.header_bar = self.create_header_bar(show_quit=show_quit, show_reset=show_reset, on_reset=on_reset)
                self.main_container.add_widget(self.header_bar)
            
            #4. setup title bar
            if title:
                self.title_bar = PixelTitleBar(title=title, show_stars=show_stars)
                self.main_container.add_widget(self.title_bar)
            else:
                self.title_bar = None

            #5. setup content card
            self.content_card = BoxLayout(
                orientation='vertical',
                padding=Layout.PIXEL_CARD_PADDING,
                spacing=dp(6)
            )
            self.main_container.add_widget(self.content_card)
            self.add_widget(self.main_container)

            #6. setup side decorations
            if show_decorations:
                self._add_decorations(decoration_type)
        else:
            # Fallback to the original plain white background screen
            with self.canvas.before:
                Color(1, 1, 1, 1)
                self.fallback_bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=lambda inst, val: setattr(self.fallback_bg_rect, 'size', val))
            self.bind(pos=lambda inst, val: setattr(self.fallback_bg_rect, 'pos', val))
            
        print(f"{self.__class__.__name__} initialized")


    def _update_bg(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _create_wrapper_header_bar(self, show_quit=False, show_reset=False, on_reset=None):
        header = BoxLayout(
            orientation='horizontal', 
            size_hint_y=0.06, 
            spacing=dp(8), 
            padding=[dp(4), dp(4), dp(4), 0]
            )
        # button_width = Layout.BUTTON_HEIGHT_STANDARD * 1.5
        if show_reset:
            reset_btn = BounceButton(text='RESET', size_hint=(0.2, 1), font_size=Typography.BUTTON_SMALL, background_color=Colors.WARNING_ORANGE, on_press=on_reset if on_reset else (lambda *_: None))
            reset_btn.bind(height=lambda inst, val: setattr(inst, 'font_size', val * 0.32))
            header.add_widget(reset_btn)
        else:
            header.add_widget(Widget(size_hint=(0.2, 1)))
        header.add_widget(Widget(size_hint_x=1)) #centre spacer
        if show_quit:
            quit_btn = BounceButton(text='QUIT', size_hint=(0.2, 1), font_size=Typography.BUTTON_SMALL, background_color=Colors.DANGER_RED_DARK, on_press=self.on_quit)
            quit_btn.bind(height=lambda inst, val: setattr(inst, 'font_size', val * 0.32))
            header.add_widget(quit_btn)
        else:
            header.add_widget(Widget(size_hint=(0.2, 1)))
        return header
    
    def _add_decorations(self, decoration_type):
        source = os.path.join(BASE_PATH, 'assets', 'ui', f'mushroom_{decoration_type}.png')
        if not os.path.exists(source):
            return
        left_deco = Image(source=source, size_hint=(None, None), allow_stretch=True, keep_ratio=True , pos_hint={'x': 0.01, 'center_y': 0.5})
        right_deco = Image(source=source, size_hint=(None, None) , allow_stretch=True, keep_ratio=True , pos_hint={'right': 0.98, 'center_y': 0.5})
        self.bind( width=lambda inst, val: setattr(left_deco, 'width', val * 0.15),
                   height=lambda inst, val: setattr(left_deco, 'height', val * 0.15)
                 )
        self.bind( width=lambda inst, val: setattr(right_deco, 'width', val * 0.15),
            height=lambda inst, val: setattr(right_deco, 'height', val * 0.15)
            )
        self.add_widget(left_deco)
        self.add_widget(right_deco)


    def set_content(self, content_widget):
        if self.enable_wrapper:
            self.content_card.clear_widgets()
            self.content_card.add_widget(content_widget)
            
    def hide_title(self):
        if self.enable_wrapper and self.title_bar:
            self.title_bar.slide_up()
            
    def show_title(self):
        if self.enable_wrapper and self.title_bar:
            self.title_bar.slide_down()



    
    # common UI components
    
    def create_title(self, text, size='standard', color=None, height=None):
    
        if color is None:
            color = Colors.PRIMARY_BLUE
        
        if height is None:
            height = Layout.TITLE_HEIGHT
        
        font_sizes = {
            'large': Typography.TITLE_LARGE,
            'standard': Typography.TITLE_STANDARD,
            'small': Typography.TITLE_SMALL
        }
        
        font_size = font_sizes.get(size, Typography.TITLE_STANDARD)
        
        title = Label(
            text=text,
            bold=True,
            color=color,
            size_hint_y=0.08,
            halign='center',
            valign='middle'  
        )
        title.bind(size=title.setter('text_size'))
        title.bind(height=lambda inst, val: setattr(inst, 'font_size', val * 0.45)) # Dynamic font size
        return title
    
    def create_subtitle(self, text, color=None, wrap=True):
        
        if color is None:
            color = Colors.TEXT_GRAY
        
        subtitle = Label(
            text=text,
            color=color,
            size_hint_y=0.05,  # Takes 5% of parent height
            halign='center',
            valign='middle'
        )
        if wrap:
            subtitle.bind(size=subtitle.setter('text_size'))
        subtitle.bind(height=lambda inst, val: setattr(inst, 'font_size', val * 0.45))
        return subtitle
    
    def create_card(self, size_hint=(1, None), height=None, padding=None, bg_color=None):
        
        if padding is None:
            padding = Layout.CARD_PADDING
        
        if bg_color is None:
            bg_color = Colors.BACKGROUND_WHITE
        
        card = BoxLayout(
            orientation='vertical',
            size_hint=size_hint,
            padding=padding
        )
        
        if height:
            card.size_hint_y = None
            card.height = height
        
        with card.canvas.before:
            Color(*bg_color)
            card.bg_rect = RoundedRectangle(radius=[Layout.CARD_RADIUS])

        with card.canvas.after:
            Color(*Colors.CARD_BORDER_REDDISH_BROWN)
            card.border_line = Line(width=dp(1.4))

        def _update_card_canvas(i, _v):
            i.bg_rect.pos = i.pos
            i.bg_rect.size = i.size
            i.border_line.rounded_rectangle = (
                i.x + dp(0.8),
                i.y + dp(0.8),
                max(i.width - dp(1.6), 0),
                max(i.height - dp(1.6), 0),
                Layout.CARD_RADIUS
            )
        
        card.bind(
            pos=_update_card_canvas,
            size=_update_card_canvas
        )
        _update_card_canvas(card, None)
        
        return card
    
    def create_button(self, text, on_press, button_type='primary', disabled=False):
        """Create button with bounce animation effect"""
        color_map = {
            'primary': Colors.PRIMARY_BLUE_DARK,
            'success': Colors.SUCCESS_GREEN,
            'danger': Colors.DANGER_RED,
            'secondary': Colors.TEXT_GRAY
        }
        
        bg_color = color_map.get(button_type, Colors.PRIMARY_BLUE_DARK)
        
        # Use BounceButton instead of regular Button for automatic bounce effect
        button = BounceButton(
            text=text,
            size_hint_y=self.size_hint_y,
            background_color=bg_color,
            disabled=disabled,
            on_press=on_press
        )
        button.bind(height=lambda inst, val: setattr(inst, 'font_size', val * 0.35))
        return button
    
    def create_input_field(self, hint_text='', multiline=False, password=False):
        
        input_field = TextInput(
            hint_text=hint_text,
            multiline=multiline,
            password=password,
            size_hint_y=0.08,
            background_color=Colors.BACKGROUND_LIGHT_GRAY,
            foreground_color=Colors.TEXT_BLACK,
            padding=[Layout.PADDING_SMALL, Layout.SPACING_SMALL]
        )
        input_field.bind(height=lambda inst, val: setattr(inst, 'font_size', val * 0.38))
        return input_field
    
    def create_scrollable_content(self, content_widget, size_hint=(1, 1)):
        
        scroll_view = ScrollView(
            size_hint=(1,1),
            do_scroll_x=False,
            do_scroll_y=True
        )
        
        scroll_view.add_widget(content_widget)
  
        scroll_container = self.create_card(
            size_hint=size_hint, #outer card
            padding=0
        )
        scroll_container.add_widget(scroll_view)
        
        return scroll_container
    

    def create_quit_button(self):
        
        quit_btn = BounceButton(
            text='QUIT',
            size_hint=(0.2,0.06),
            background_color=Colors.DANGER_RED_DARK,
            on_press=self.on_quit
        )
        quit_btn.bind(height=lambda inst, val: setattr(inst, 'font_size', val * 0.32))
        return quit_btn
    
    def create_header_bar(self, show_quit=True, show_reset=False, on_reset=None, title=None):
        
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.06,
            # height=Layout.BUTTON_HEIGHT_SMALL,
            spacing=Layout.SPACING_SMALL,
            padding=[Layout.PADDING_SMALL, Layout.PADDING_SMALL, Layout.PADDING_SMALL, 0]
        )
        
        # LEFT COLUMN: Reset button or spacer
        if show_reset:
            reset_btn = BounceButton(
                text='RESET',
                size_hint=(0.2, 1),
                background_color=Colors.WARNING_ORANGE,
                font_size=Typography.BUTTON_SMALL,
                on_press=on_reset
            )
            reset_btn.bind(height=lambda inst, val: setattr(inst, 'font_size', val * 0.32))
            header.add_widget(reset_btn)
        else:
            # Empty spacer to maintain 3-column layout
            left_spacer = BoxLayout(size_hint=(0.2, 1))
            header.add_widget(left_spacer)
        
        # CENTER COLUMN: Title or spacer (takes remaining space)
        if title:
            title_label = Label(
                text=title,
                font_size=Typography.TITLE_STANDARD,
                color=Colors.PRIMARY_BLUE,
                bold=True,
                halign='center',
                valign='middle', 
                size_hint_x=1  # Take remaining space to center properly
            )
            title_label.bind(height=lambda inst, val: setattr(inst, 'font_size', val * 0.32))
            header.add_widget(title_label)
        else:
            # Spacer to maintain 3-column layout
            center_spacer = BoxLayout(size_hint_x=1)
            header.add_widget(center_spacer)
        
        # RIGHT COLUMN: Quit button or spacer
        if show_quit:
            quit_btn = BounceButton(
                text='QUIT',
                size_hint=(0.2, 1),
                background_color=Colors.DANGER_RED_DARK,
                font_size=Typography.BUTTON_SMALL,
                on_press=self.on_quit
            )
            quit_btn.bind(height=lambda inst, val: setattr(inst, 'font_size', val * 0.32))
            header.add_widget(quit_btn)
        else:
            # Empty spacer to maintain 3-column layout
            right_spacer = BoxLayout(size_hint=(0.2, 1))
            header.add_widget(right_spacer)
        
        return header
    

    
    def on_quit(self, instance):
        """
        Quit button handler
        Override this method in subclasses for custom quit behavior
        """
        SoundManager.play('negative')
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        content.add_widget(Label(text='Are you sure you want to quit?', color=Colors.TEXT_BLACK))
        
        btn_row = BoxLayout(spacing=dp(10), size_hint_y=0.4)
        
        popup = Popup(title='Confirm Quit', content=content, size_hint=(0.6, 0.3), auto_dismiss=False)
        
        yes_btn = Button(text='Yes', on_press=lambda *_: App.get_running_app().stop())
        no_btn = Button(text='No', on_press=lambda *_: popup.dismiss())
        
        btn_row.add_widget(yes_btn)
        btn_row.add_widget(no_btn)
        content.add_widget(btn_row)
        
        popup.open()
        print(f" Quit requested from {self.__class__.__name__}")
        # TODO: Add confirmation dialog if needed
        # App.get_running_app().stop()
    
    def on_pre_enter(self, *args):
        """Called before screen is displayed"""
        print(f"  Entering {self.__class__.__name__}")
        super(BaseScreen, self).on_pre_enter(*args)
    
    def on_leave(self, *args):
        """Called when leaving screen"""
        print(f"  Leaving {self.__class__.__name__}")
        super(BaseScreen, self).on_leave(*args)

