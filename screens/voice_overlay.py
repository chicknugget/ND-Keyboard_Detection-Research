# screens/voice_overlay.py

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
import os

from screens.config import BASE_PATH

from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock


class VoiceToggleButton(ButtonBehavior, Image):
    """Floating mute/unmute button that plays per-screen voice audio."""

    # map screen names to voice file names
    VOICE_MAP = {
        'consent': 'voice_consent.mp3',
        'demographics': 'voice_demographic.mp3',
        'instructions': 'voice_instruction.mp3',

        # 'post_task_relaxation': 'voice_feedback.mp3',
        # 'post_task_happy': 'voice_feedback.mp3',
        # 'post_task_sad': 'voice_feedback.mp3',
        # 'post_task_boredom': 'voice_feedback.mp3',
        # 'post_task_stress': 'voice_feedback.mp3',
        # 'post_task_frustrated': 'voice_feedback.mp3',
        # # debriefing screens: debriefing_frustrated, debriefing_stress, etc.
        # 'debriefing_frustrated': 'voice_debrief.mp3',
        # 'debriefing_stress': 'voice_debrief.mp3',
        'debriefing': 'voice_debrief.mp3',
        'post_task': 'voice_feedback.mp3',
    }

    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.muted = False
        self.current_voice = None

        # button appearance
        sound_dir = os.path.join(BASE_PATH, 'assets', 'sound')
        self.unmute_icon = os.path.join(sound_dir, 'unmute.png')
        self.mute_icon = os.path.join(sound_dir, 'mute.png')
        self.source = self.unmute_icon

        # size and position   top-left corner
        self.size_hint = (None, None)
        self.size = (48, 48)
        self.pos = ( 12, Window.height-60)


        # add dark background for visibility
        with self.canvas.before:
            # Color(0.2, 0.2, 0.2, 0.7) 
            Color(1, 1, 1, 0.25) 
            self._bg_rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[24]
            )
        self.bind(
            pos=lambda inst, val: setattr(self._bg_rect, 'pos', val),
            size=lambda inst, val: setattr(self._bg_rect, 'size', val)
        )

        # pre load all voice sounds
        self._voices = {}
        for key, filename in self.VOICE_MAP.items():
            path = os.path.join(sound_dir, filename)
            sound = SoundLoader.load(path)
            if sound:
                sound.loop = False
                self._voices[key] = sound

        # reposition on window resize
        Window.bind(size=self._reposition)

        # Listen for screen changes
        self.screen_manager.bind(current=self._on_screen_change)


        self._play_event = None
        Clock.schedule_once(lambda dt: self._on_screen_change(None, self.screen_manager.current), 1)

    def _reposition(self, instance, value):
        """Keep button in bottom-right corner on resize."""
        self.pos = ( 12, value[1] - 60)

    def _get_voice_key(self, screen_name):
        """
        Match screen name to a voice key.
        Handles exact matches and prefix matches
        (e.g. 'post_task_happy' matches 'post_task').
        """
        # try exact match first
        if screen_name in self._voices:
            return screen_name

        # try prefix match
        for key in self.VOICE_MAP:
            if screen_name.startswith(key):
                return key

        return None
    


    def _on_screen_change(self, instance, screen_name):
        """Stop current voice, start new one after 1-second delay."""
        self._stop_current()
        
        # Cancel any pending scheduled play
        if hasattr(self, '_play_event') and self._play_event:
            self._play_event.cancel()

        if self.muted:
            return

        voice_key = self._get_voice_key(screen_name)
        if voice_key and voice_key in self._voices:
            self.opacity = 1.0
            self.disabled = False
            # Delay playback by 1 second
            self._play_event = Clock.schedule_once(
                lambda dt: self._start_voice(voice_key), 1
            )
        else:
            self.current_voice = None
            self.opacity = 0.5
            self.disabled = False

    def _start_voice(self, voice_key):
        """Actually start playing the voice audio."""
        if not self.muted and voice_key in self._voices:
            self.current_voice = self._voices[voice_key]
            self.current_voice.play()

    # def _on_screen_change(self, instance, screen_name):
    #     """Stop current voice, start new one if screen has a voice."""
    #     self._stop_current()

    #     if self.muted:
    #         return

    #     voice_key = self._get_voice_key(screen_name)
    #     if voice_key and voice_key in self._voices:
    #         self.current_voice = self._voices[voice_key]
    #         self.current_voice.play()
    #         self.opacity = 1.0
    #         self.disabled=False
    #     else:
    #         # no voice for this screen - hide button or keep visible
    #         self.current_voice = None
    #         self.opacity = 0.5  # hide button
    #         self.disabled=False

    
    def _stop_current(self):
        if hasattr(self, '_play_event') and self._play_event:
            self._play_event.cancel()
            self._play_event = None
        if self.current_voice:
            self.current_voice.stop()
            self.current_voice = None

    def on_press(self):
        """Toggle mute/unmute on tap."""
        self.muted = not self.muted

        if self.muted:
            self.source = self.mute_icon
            self._stop_current()
        else:
            self.source = self.unmute_icon
            # play the voice for the current screen
            screen_name = self.screen_manager.current
            voice_key = self._get_voice_key(screen_name)
            if voice_key and voice_key in self._voices:
                self.current_voice = self._voices[voice_key]
                self.current_voice.play()

    def detach(self):
        """Clean up — call when app closes."""
        self._stop_current()
        Window.unbind(size=self._reposition)