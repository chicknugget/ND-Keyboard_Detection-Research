# screens/base_screen.py 


from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle, Rectangle

from screens.config import Colors, Layout, Typography, AppConfig


class BaseScreen(Screen):
    """
    Base class for all screens in the app
    Provides common UI components and functionality
    """
    
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        
        # Add white background to all screens by default
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White 
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=lambda instance, value: setattr(self.bg_rect, 'size', value))
        self.bind(pos=lambda instance, value: setattr(self.bg_rect, 'pos', value))
        
        # Lock orientation when screen is created
        AppConfig.lock_orientation(AppConfig.ORIENTATION)
        
        # Debug logging
        print(f"{self.__class__.__name__} initialized")
    

    # common UI components
    
    def create_title(self, text, size='standard', color=None, height=None):
        """
        Create a standardized title label
        
        Args:
            text (str): Title text
            size (str): 'large', 'standard', or 'small'
            color (tuple): RGBA color (default: PRIMARY_BLUE)
            height (float): Custom height (default: from Layout)
        
        Returns:
            Label: Configured title label
        """
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
            font_size=font_size,
            bold=True,
            color=color,
            size_hint_y=None,
            height=height,
            halign='center',
            valign='middle'  
        )
        title.bind(size=title.setter('text_size'))
        return title
    
    def create_subtitle(self, text, color=None, wrap=True):
        """
        Create a subtitle/hint label
        
        Args:
            text (str): Subtitle text
            color (tuple): RGBA color (default: TEXT_GRAY)
            wrap (bool): Whether to wrap text
        
        Returns:
            Label: Configured subtitle label
        """
        if color is None:
            color = Colors.TEXT_GRAY
        
        subtitle = Label(
            text=text,
            font_size=Typography.BODY_STANDARD,
            color=color,
            halign='center',
            valign='middle'
        )
        
        if wrap:
            subtitle.bind(size=subtitle.setter('text_size'))
        
        return subtitle
    
    def create_card(self, size_hint=(1, None), height=None, padding=None, bg_color=None):
        """
        Create a card container (white rounded rectangle background)
        
        Args:
            size_hint (tuple): Size hint for the card
            height (float): Card height
            padding (float or list): Card padding
            bg_color (tuple): Background color (default: BACKGROUND_WHITE)
        
        Returns:
            BoxLayout: Card container with rounded background
        """
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
        
        # Add rounded rectangle background
        with card.canvas.before:
            Color(*bg_color)
            card.bg_rect = RoundedRectangle(radius=[Layout.CARD_RADIUS])
        
        card.bind(
            pos=lambda i, v: setattr(card.bg_rect, 'pos', i.pos),
            size=lambda i, v: setattr(card.bg_rect, 'size', i.size)
        )
        
        return card
    
    def create_button(self, text, on_press, button_type='primary', disabled=False):
        """
        Create a standardized button
        
        Args:
            text (str): Button text
            on_press (callable): Button press handler
            button_type (str): 'primary', 'success', 'danger', 'secondary'
            disabled (bool): Whether button is disabled
        
        Returns:
            Button: Configured button
        """
        color_map = {
            'primary': Colors.PRIMARY_BLUE_DARK,
            'success': Colors.SUCCESS_GREEN,
            'danger': Colors.DANGER_RED,
            'secondary': Colors.TEXT_GRAY
        }
        
        bg_color = color_map.get(button_type, Colors.PRIMARY_BLUE_DARK)
        
        button = Button(
            text=text,
            font_size=Typography.BUTTON_STANDARD,
            size_hint_y=None,
            height=Layout.BUTTON_HEIGHT_STANDARD,
            background_color=bg_color,
            disabled=disabled,
            on_press=on_press
        )
        
        return button
    
    def create_input_field(self, hint_text='', multiline=False, password=False):
        """
        Create a standardized input field
        
        Args:
            hint_text (str): Placeholder text
            multiline (bool): Allow multiple lines
            password (bool): Password field (masked)
        
        Returns:
            TextInput: Configured input field
        """
        input_field = TextInput(
            hint_text=hint_text,
            multiline=multiline,
            password=password,
            font_size=Typography.BODY_STANDARD,
            size_hint_y=None,
            height=Layout.INPUT_HEIGHT,
            background_color=Colors.BACKGROUND_LIGHT_GRAY,
            foreground_color=Colors.TEXT_BLACK,
            padding=[Layout.PADDING_SMALL, Layout.SPACING_SMALL]
        )
        
        return input_field
    
    def create_scrollable_content(self, content_widget, size_hint=(1, 1)):
        """
        Wrap content in a scrollable container
        
        Args:
            content_widget (Widget): Widget to make scrollable
            size_hint (tuple): Size hint for scroll container
        
        Returns:
            ScrollView: Scrollable container with content
        """
        scroll_view = ScrollView(
            size_hint=size_hint,
            do_scroll_x=False,
            do_scroll_y=True
        )
        
        scroll_view.add_widget(content_widget)
        
        # Wrap in card for consistent styling
        scroll_container = self.create_card(
            size_hint=size_hint,
            padding=0
        )
        scroll_container.add_widget(scroll_view)
        
        return scroll_container
    
    def create_quit_button(self, size_hint=(None, None), size=None):
        """
        Create a standardized quit button
        Appears in top-right corner or as separate button
        
        Args:
            size_hint (tuple): Size hint for button
            size (tuple): Fixed size for button
        
        Returns:
            Button: Quit button
        """
        if size is None:
            size = (Layout.BUTTON_HEIGHT_STANDARD * 1.5, Layout.BUTTON_HEIGHT_TINY)
        
        quit_btn = Button(
            text='QUIT',
            size_hint=size_hint,
            size=size,
            background_color=Colors.DANGER_RED_DARK,
            font_size=Typography.BUTTON_SMALL,
            on_press=self.on_quit
        )
        return quit_btn
    
    def create_header_bar(self, show_quit=True, show_reset=False, on_reset=None, title=None):
        """
        Create a header bar with 3-column layout: [RESET] [TITLE] [QUIT]
        Each element can be independently shown/hidden
        
        Args:
            show_quit (bool): Show quit button in top-right
            show_reset (bool): Show reset button in top-left
            on_reset (callable): Reset button callback (required if show_reset=True)
            title (str): Optional title to display in center of header
        
        Returns:
            BoxLayout: Header bar with 3-column layout
        """
        from kivy.uix.label import Label
        
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=Layout.BUTTON_HEIGHT_SMALL,
            spacing=Layout.SPACING_SMALL,
            padding=[Layout.PADDING_SMALL, Layout.PADDING_SMALL, Layout.PADDING_SMALL, 0]
        )
        
        # LEFT COLUMN: Reset button or spacer
        if show_reset:
            reset_btn = Button(
                text='RESET',
                size_hint=(None, 1),
                width=Layout.BUTTON_HEIGHT_STANDARD * 1.5,
                background_color=Colors.WARNING_ORANGE,
                font_size=Typography.BUTTON_SMALL,
                on_press=on_reset
            )
            header.add_widget(reset_btn)
        else:
            # Empty spacer to maintain 3-column layout
            left_spacer = BoxLayout(size_hint=(None, 1), width=Layout.BUTTON_HEIGHT_STANDARD * 1.5)
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
            header.add_widget(title_label)
        else:
            # Spacer to maintain 3-column layout
            center_spacer = BoxLayout(size_hint_x=1)
            header.add_widget(center_spacer)
        
        # RIGHT COLUMN: Quit button or spacer
        if show_quit:
            quit_btn = Button(
                text='QUIT',
                size_hint=(None, 1),
                width=Layout.BUTTON_HEIGHT_STANDARD * 1.5,
                background_color=Colors.DANGER_RED_DARK,
                font_size=Typography.BUTTON_SMALL,
                on_press=self.on_quit
            )
            header.add_widget(quit_btn)
        else:
            # Empty spacer to maintain 3-column layout
            right_spacer = BoxLayout(size_hint=(None, 1), width=Layout.BUTTON_HEIGHT_STANDARD * 1.5)
            header.add_widget(right_spacer)
        
        return header
    
    
    # COMMON EVENT HANDLERS
    
    def on_quit(self, instance):
        """
        Quit button handler
        Override this method in subclasses for custom quit behavior
        """
        print(f" Quit requested from {self.__class__.__name__}")
        # TODO: Add confirmation dialog if needed
        App.get_running_app().stop()
    
    def on_pre_enter(self, *args):
        """Called before screen is displayed"""
        print(f"  Entering {self.__class__.__name__}")
        super(BaseScreen, self).on_pre_enter(*args)
    
    def on_leave(self, *args):
        """Called when leaving screen"""
        print(f"  Leaving {self.__class__.__name__}")
        super(BaseScreen, self).on_leave(*args)
