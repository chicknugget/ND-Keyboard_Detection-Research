# screens/pixel_ui_wrapper.py
"""
Pixel-art UI wrapper components for child-friendly game theme
Provides: PixelFrame (main wrapper), PixelCard (content container), 
         PixelTitleBar (decorative title), BounceButton behavior
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.core.text import LabelBase
from kivy.app import App
import os

from screens.config import Colors, Layout, Typography, BASE_PATH, PixelUI
from screens.base_screen import BounceButton

# Register pixel fonts (already done in config, but ensure here too)
try:
    LabelBase.register(name='PixelTitle', fn_regular=os.path.join(BASE_PATH, 'assets', 'fonts', 'PrStart.ttf'))
    LabelBase.register(name='PixelBody', fn_regular=os.path.join(BASE_PATH, 'assets', 'fonts', 'NeuePixelSans.ttf'))
except:
    pass  # Fallback to default if fonts not found

# Asset paths (using BASE_PATH from config)
UI_ASSETS = {
    'green_mosaic': os.path.join(BASE_PATH, 'assets', 'ui', 'green_mosaic.png'),
    'beige_light': os.path.join(BASE_PATH, 'assets', 'ui', 'beige_light.png'),
    'mushroom_handsup': os.path.join(BASE_PATH, 'assets', 'ui', 'mushroom_handsup.png'),
    'mushroom_handsdown': os.path.join(BASE_PATH, 'assets', 'ui', 'mushroom_handsdown.png'),
    'star': os.path.join(BASE_PATH, 'assets', 'ui', 'star.png'),
}


class BounceBehavior:
    """Mixin that adds bounce animation to buttons using Kivy Animation"""
    
    def trigger_bounce(self, instance):
        """Trigger bounce: scale down to 0.95 then back to 1.0 using size animation"""
        original_width = self.width
        original_height = self.height
        
        # Cancel any existing animation
        Animation.cancel_all(self, 'size')
        
        # Shrink slightly
        target_width = original_width * 0.95
        target_height = original_height * 0.95
        
        # Create animation sequence
        anim = Animation(size=(target_width, target_height), duration=0.05, t='out_quad')
        anim += Animation(size=(original_width, original_height), duration=0.15, t='out_bounce')
        
        anim.start(self)


class PixelCard(BoxLayout):
    """
    Content container for pixel screens.
    Background and border visuals are intentionally removed so content can
    utilize maximum screen area.
    """
    content_area = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = Layout.PIXEL_CARD_PADDING
        self.spacing = dp(6)
        
        # Create content area
        self.content_area = BoxLayout(
            orientation='vertical',
            padding=Layout.PIXEL_CONTENT_PADDING,  # Internal padding
            spacing=dp(10)
        )
        
        # Build canvas with background and border
        self._update_canvas()
        self.bind(pos=self._update_canvas, size=self._update_canvas)
        
        super().add_widget(self.content_area)
    
    def _update_canvas(self, *args):
        self.canvas.before.clear()

    def add_widget(self, widget, index=0):
        """Override to add to content_area instead"""
        if widget == self.content_area:
            super().add_widget(widget, index)
        else:
            self.content_area.add_widget(widget, index)
    
    def set_content(self, content_widget):
        """Set the main content widget"""
        self.content_area.clear_widgets()
        self.content_area.add_widget(content_widget)


class PixelTitleBar(BoxLayout):
    """
    Fixed title bar with optional star decorations
    Slides up/down with animation
    """
    title_text = StringProperty('')
    show_stars = True
    visible = True
    
    def __init__(self, title='', show_stars=True, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = Layout.PIXEL_TITLE_HEIGHT
        self.title_text = title
        self.show_stars = show_stars
        self.padding = [dp(10), dp(5)]
        self.spacing = dp(10)
        
        self._build()
    
    def _build(self):
        # Left star or spacer
        if self.show_stars and os.path.exists(UI_ASSETS['star']):
            self.left_star = Image(
                source=UI_ASSETS['star'],
                size_hint=(None, None),
                size=(Layout.PIXEL_STAR_SIZE, Layout.PIXEL_STAR_SIZE),
                allow_stretch=True,
                keep_ratio=True
            )
            self.add_widget(self.left_star)
        else:
            self.add_widget(Widget(size_hint_x=0.1))
        
        # Title label
        self.title_label = Label(
            text=self.title_text,
            font_name=PixelUI.FONT_TITLE,
            font_size=Typography.PIXEL_TITLE_STANDARD,
            color=Colors.TEXT_BLACK,
            halign='center',
            valign='middle',
            size_hint_x=1,
            bold=True
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        self.add_widget(self.title_label)
        
        # Right star or spacer
        if self.show_stars and os.path.exists(UI_ASSETS['star']):
            self.right_star = Image(
                source=UI_ASSETS['star'],
                size_hint=(None, None),
                size=(Layout.PIXEL_STAR_SIZE, Layout.PIXEL_STAR_SIZE),
                allow_stretch=True,
                keep_ratio=True
            )
            self.add_widget(self.right_star)
        else:
            self.add_widget(Widget(size_hint_x=0.1))
    
    def set_title(self, text):
        self.title_text = text
        self.title_label.text = text
    
    def slide_up(self, duration=0.3):
        """Slide up out of view"""
        if self.visible:
            target_y = self.parent.height if self.parent else 800
            anim = Animation(y=target_y, duration=duration)
            anim.start(self)
            self.visible = False
    
    def slide_down(self, duration=0.3):
        """Slide back into view"""
        if not self.visible:
            target_y = (self.parent.height - self.height) if self.parent else 50
            anim = Animation(y=target_y, duration=duration)
            anim.start(self)
            self.visible = True


class PixelFrame(FloatLayout):
    """
    Main wrapper frame providing:
    - Green mosaic background
    - Centered PixelCard content area
    - Optional side decorations
    - Fixed title bar at top
    """
    content_area = ObjectProperty(None)
    title_bar = ObjectProperty(None)
    card = ObjectProperty(None)
    
    def __init__(self, title='', show_stars=True, show_decorations=False,
                 decoration_type='handsup', show_header=True,
                 show_quit=False, show_reset=False, on_quit=None,
                 on_reset=None, **kwargs):
        super().__init__(**kwargs)
        
        # Background
        self._setup_background()
        
        # Main container (centered)
        self.main_container = BoxLayout(
            orientation='vertical',
            size_hint=(0.965, 0.965),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=dp(6)
        )

        # Header row (top), title stays below header for all screens.
        if show_header:
            self.header_bar = self._create_header_bar(
                show_quit=show_quit,
                show_reset=show_reset,
                on_quit=on_quit,
                on_reset=on_reset
            )
            self.main_container.add_widget(self.header_bar)

        # Title bar (fixed at top of container)
        if title:
            self.title_bar = PixelTitleBar(title=title, show_stars=show_stars)
            self.main_container.add_widget(self.title_bar)
        
        # Content card (expands to fill)
        self.card = PixelCard()
        self.content_area = self.card.content_area
        self.main_container.add_widget(self.card)
        
        # Side decorations (if enabled)
        if show_decorations:
            self._add_decorations(decoration_type)
        
        self.add_widget(self.main_container)

    def _create_header_bar(self, show_quit=False, show_reset=False, on_quit=None, on_reset=None):
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=Layout.BUTTON_HEIGHT_SMALL,
            spacing=dp(8),
            padding=[dp(4), dp(4), dp(4), 0]
        )

        button_width = Layout.BUTTON_HEIGHT_STANDARD * 1.5

        if show_reset:
            reset_btn = BounceButton(
                text='RESET',
                size_hint=(None, 1),
                width=button_width,
                font_size=Typography.BUTTON_SMALL,
                background_color=Colors.WARNING_ORANGE,
                on_press=on_reset if on_reset else (lambda *_: None)
            )
            header.add_widget(reset_btn)
        else:
            header.add_widget(Widget(size_hint=(None, 1), width=button_width))

        header.add_widget(Widget(size_hint_x=1))

        if show_quit:
            quit_btn = BounceButton(
                text='QUIT',
                size_hint=(None, 1),
                width=button_width,
                font_size=Typography.BUTTON_SMALL,
                background_color=Colors.DANGER_RED_DARK,
                on_press=on_quit if on_quit else self._default_quit
            )
            header.add_widget(quit_btn)
        else:
            header.add_widget(Widget(size_hint=(None, 1), width=button_width))

        return header

    def _default_quit(self, *_):
        App.get_running_app().stop()
    
    def _setup_background(self):
        """Set up green mosaic background"""
        with self.canvas.before:
            if os.path.exists(UI_ASSETS['green_mosaic']):
                Color(1, 1, 1, 1)
                self.bg_rect = Rectangle(
                    source=UI_ASSETS['green_mosaic'],
                    pos=self.pos,
                    size=self.size
                )
            else:
                # Fallback: nice green gradient color
                Color(0.4, 0.7, 0.3, 1)
                self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self._update_bg, size=self._update_bg)
    
    def _update_bg(self, instance, value):
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size
    
    def _add_decorations(self, decoration_type):
        """Add floating side decorations"""
        if decoration_type == 'handsup':
            source = UI_ASSETS['mushroom_handsup']
        elif decoration_type == 'handsdown':
            source = UI_ASSETS['mushroom_handsdown']
        else:
            return
        
        if not os.path.exists(source):
            return
        
        # Left decoration (positioned at left edge, floating)
        left_deco = Image(
            source=source,
            size_hint=(None, None),
            size=(Layout.PIXEL_MUSHROOM_SIZE, Layout.PIXEL_MUSHROOM_SIZE),
            pos_hint={'x': 0.02, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
        
        # Right decoration (positioned at right edge, floating)
        right_deco = Image(
            source=source,
            size_hint=(None, None),
            size=(Layout.PIXEL_MUSHROOM_SIZE, Layout.PIXEL_MUSHROOM_SIZE),
            pos_hint={'right': 0.98, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
        
        self.add_widget(left_deco)
        self.add_widget(right_deco)
        self.decorations = [left_deco, right_deco]
    
    def set_content(self, content_widget):
        """Set the main content into the card"""
        self.card.set_content(content_widget)
    
    def hide_title(self):
        """Slide title up out of view"""
        if self.title_bar:
            self.title_bar.slide_up()
    
    def show_title(self):
        """Slide title back down"""
        if self.title_bar:
            self.title_bar.slide_down()


class PixelFrameWithBottomDeco(PixelFrame):
    """Special variant with decorations below title (for completion screen)"""
    
    def __init__(self, title='', show_stars=True, bottom_decoration='handsdown', **kwargs):
        super().__init__(title='', show_stars=False, **kwargs)  # No default title
        
        # Rebuild with custom layout
        self.main_container.clear_widgets()
        
        # Title with stars
        if title:
            self.title_bar = PixelTitleBar(title=title, show_stars=show_stars)
            self.main_container.add_widget(self.title_bar)
        
        # Bottom decoration row
        if bottom_decoration and os.path.exists(UI_ASSETS.get(f'mushroom_{bottom_decoration}', '')):
            deco_row = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(80),
                spacing=dp(20),
                padding=[dp(20), dp(5)]
            )
            
            # Center the decoration
            source = UI_ASSETS.get(f'mushroom_{bottom_decoration}', '')
            if source and os.path.exists(source):
                deco_img = Image(
                    source=source,
                    size_hint=(None, None),
                    size=(dp(80), dp(80)),
                    allow_stretch=True,
                    keep_ratio=True,
                    pos_hint={'center_x': 0.5}
                )
                deco_row.add_widget(Widget())  # Spacer
                deco_row.add_widget(deco_img)
                deco_row.add_widget(Widget())  # Spacer
            
            self.main_container.add_widget(deco_row)
        
        # Content card
        self.card = PixelCard()
        self.content_area = self.card.content_area
        self.main_container.add_widget(self.card)


class DebriefingFrame(PixelFrame):
    """Special frame for debriefing with edge mushrooms and centered content"""
    
    def __init__(self, title='', **kwargs):
        super().__init__(title=title, show_stars=True, **kwargs)
        
        # Add floating mushrooms at edges (outside the card)
        self._add_edge_mushrooms()
    
    def _add_edge_mushrooms(self):
        """Add mushrooms floating at screen edges, beside the message card"""
        source = UI_ASSETS['mushroom_handsup']
        if not os.path.exists(source):
            return
        
        # Left mushroom at left edge, vertically centered
        left_mush = Image(
            source=source,
            size_hint=(None, None),
            size=(dp(120), dp(120)),
            pos_hint={'x': 0.01, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
        
        # Right mushroom at right edge, vertically centered  
        right_mush = Image(
            source=source,
            size_hint=(None, None),
            size=(dp(120), dp(120)),
            pos_hint={'right': 0.99, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
        
        # Add to frame (not main_container, so they float at edges)
        self.add_widget(left_mush, index=1)
        self.add_widget(right_mush, index=1)
        self.edge_mushrooms = [left_mush, right_mush]
