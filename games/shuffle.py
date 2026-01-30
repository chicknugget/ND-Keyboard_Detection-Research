from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', True)

from kivy.app import App
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty
import random


random_win = random.randint(1, 4)
 
class ImageButton(ButtonBehavior, Image):
    pass

class ShufflingGame(FloatLayout):
    speed = NumericProperty(0.5)
    current_round = 1

    def __init__(self, level = 0, rigged=None, speed=0.5, no_of_glasses=3, points_show=True, total_rounds=10, **kwargs):
        super(ShufflingGame, self).__init__(**kwargs)
        self.level = level
        self.rigged = rigged
        self.speed = speed
        self.no_of_glasses = no_of_glasses
        self.total_rounds = total_rounds
        self.points_show = points_show
        self.total_shuffles = 3 
        self.points = 0
        
        with self.canvas.before:
            Color(97/255, 112/255, 44/255, 1)   
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.level_label = Label(text=f"Level {self.level}:", 
                   font_size='30sp',
                   font_name = 'PrStart.ttf',
                   color=(46/255, 34/255, 4/255, 1), 
                   size_hint=(0.8, 0.1), 
                   pos_hint={'center_x': 0.5, 'top': 0.9})
        self.add_widget(self.level_label)

        self.round_label = Label(text=f"Round {self.current_round}:", 
                   font_size='20sp',
                   font_name = 'PrStart.ttf',
                   color=(64/255, 48/255, 6/255, 1), 
                   size_hint=(0.8, 0.1), 
                   pos_hint={'center_x': 0.5, 'top': 0.8})
        self.add_widget(self.round_label)

        self.points_label = Label(text=f"Points: {self.points}", 
                   font_size='10sp',
                   font_name = 'PrStart.ttf',
                   color=(64/255, 48/255, 6/255, 1), 
                   size_hint=(0.8, 0.1), 
                   pos_hint={'center_x': 0.5, 'top': 0.75},
                   opacity=1 if self.points_show else 0)
        self.add_widget(self.points_label)

        self.find_ball = Label(text="Find the ball!", 
                   font_size='15sp',
                   font_name = 'PrStart.ttf',
                   color=(48/255, 42/255, 3/255, 1),
                   size_hint=(0.6, 0.1),
                   pos_hint={'center_x': 0.5, 'top': 0.7},
                   opacity=0)
        self.add_widget(self.find_ball)

        self.setup_game()

    def setup_game(self):
        if self.no_of_glasses == 1:
            self.lanes = [0.5]
        else:
            self.lanes = [0.1 + (i * 0.8 / (self.no_of_glasses - 1)) for i in range(self.no_of_glasses)]
        self.glasses = []
        self.correct_index = random.randint(0, self.no_of_glasses - 1)
        self.shuffles_done = 0
        self.can_click = False

        width_hint = 0.75 / self.no_of_glasses

        if hasattr(self, 'ball'): self.remove_widget(self.ball)
        self.ball = Image(
            source='ball.png', 
            size_hint=(width_hint*0.6, 0.1), 
            opacity=0,
            pos_hint={'center_x': self.lanes[self.correct_index], 'center_y': 0.4}
        )
        self.add_widget(self.ball)

        for i in range(self.no_of_glasses):
            width_hint = 0.75 / self.no_of_glasses
            btn = ImageButton(
                source='cup.png', 
                size_hint=(width_hint, 0.2),
                pos_hint={'center_x': self.lanes[i], 'center_y': 0.4}
            )
            if self.rigged == None:
                btn.bind(on_release=self.check_guess)
            elif self.rigged == "rig_win":
                btn.bind(on_release=self.rigged_win)
            elif self.rigged == "rig_lose":
                btn.bind(on_release=self.rig_lose)
            elif self.rigged == "rig_nwin_oloss":
                btn.bind(on_release=self.rig_nwin_oloss)
            elif self.rigged == "rig_owin_nloss":
                btn.bind(on_release=lambda instance: self.rig_owin_nloss(instance, random_win))
            
            self.add_widget(btn)
            self.glasses.append(btn)

        self.correct_glass = self.glasses[self.correct_index]
        Clock.schedule_once(self.initial_reveal, 1.0)

    def next_round(self):
        if self.current_round < self.total_rounds:
            self.current_round += 1
            self.round_label.text = f"Round {self.current_round}:"
            
            for glass in self.glasses:
                self.remove_widget(glass)
            self.find_ball.opacity = 0
            self.setup_game()
        else:
            self.round_label.text = "Game Over"
            self.next_level_button=Button(text="Next Level?",
                                     size_hint=(0.7, 0.1),
                                     pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                     font_size='20sp',
                                     font_name = 'PrStart.ttf',
                                     background_color=(0.38, 0.26, 0.04, 1),
                                     color=(232/255, 208/255, 149/255, 1))
            self.add_widget(self.next_level_button)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def initial_reveal(self, dt):
        self.ball.opacity = 1
        up_y, down_y = 0.55, 0.4
        reveal = Animation(pos_hint={'center_y': up_y}, duration=0.5) + \
                 Animation(pos_hint={'center_y': up_y}, duration=0.8) + \
                 Animation(pos_hint={'center_y': down_y}, duration=0.5)
        reveal.bind(on_complete=self.start_shuffle_phase)
        reveal.start(self.correct_glass)

    def start_shuffle_phase(self, *args):
        self.ball.opacity = 0 
        self.shuffle_glasses()

    def shuffle_glasses(self, *args):
        current_positions = [g.pos_hint['center_x'] for g in self.glasses]
        random.shuffle(current_positions)
        for i, glass in enumerate(self.glasses):
            target_x = current_positions[i]
            anim = Animation(pos_hint={'center_x': target_x}, duration=self.speed, t='in_out_quad')
            if glass == self.correct_glass:
                Animation(pos_hint={'center_x': target_x}, duration=self.speed, t='in_out_quad').start(self.ball)
            if i == len(self.glasses) - 1:
                anim.bind(on_complete=self.on_shuffle_step_complete)
            anim.start(glass)

    def on_shuffle_step_complete(self, *args):
        self.shuffles_done += 1
        if self.shuffles_done < self.total_shuffles:
            self.shuffle_glasses()
        else:
            self.find_ball.opacity = 1
            self.can_click = True

    def end_turn(self):
        Clock.schedule_once(lambda dt: self.next_round(), 2.0)

    def rig_nwin_oloss(self, instance):
        if self.current_round < self.total_rounds:
            if not self.can_click: return
            self.can_click = False
            self.ball.pos_hint = {'center_x': instance.pos_hint['center_x'], 'center_y': 0.4}
            self.ball.opacity = 1
            Animation(pos_hint={'center_y': 0.55}, duration=0.4).start(instance)
            self.points += 10
            self.points_label.text = f"Points: {self.points}"
        else:
            if not self.can_click: return
            self.can_click = False
            other_glasses = [g for g in self.glasses if g != instance]
            wrong_glass = random.choice(other_glasses)
            self.ball.pos_hint = {'center_x': wrong_glass.pos_hint['center_x'], 'center_y': 0.4}
            Animation(pos_hint={'center_y': 0.55}, duration=0.4).start(instance)
            Clock.schedule_once(lambda dt: Animation(pos_hint={'center_y': 0.4}, duration=0.4).start(instance), 1)
            self.points -= 10
            self.points_label.text = f"Points: {self.points}"
        self.end_turn()

    def rig_owin_nloss(self, instance, random_win):
        if self.current_round == random_win:
            if not self.can_click: return
            self.can_click = False
            self.ball.pos_hint = {'center_x': instance.pos_hint['center_x'], 'center_y': 0.4}
            self.ball.opacity = 1
            Animation(pos_hint={'center_y': 0.55}, duration=0.4).start(instance)
            self.points += 10
            self.points_label.text = f"Points: {self.points}"
        else:
            if not self.can_click: return
            self.can_click = False
            other_glasses = [g for g in self.glasses if g != instance]
            wrong_glass = random.choice(other_glasses)
            self.ball.pos_hint = {'center_x': wrong_glass.pos_hint['center_x'], 'center_y': 0.4}
            Animation(pos_hint={'center_y': 0.55}, duration=0.4).start(instance)
            Clock.schedule_once(lambda dt: Animation(pos_hint={'center_y': 0.4}, duration=0.4).start(instance), 1)
            self.points -= 10
            self.points_label.text = f"Points: {self.points}"
        self.end_turn()

    def check_guess(self, instance):
        if not self.can_click: return
        self.can_click = False
        self.ball.pos_hint = {'center_x': self.correct_glass.pos_hint['center_x'], 'center_y': 0.4}
        Animation(pos_hint={'center_y': 0.55}, duration=0.4).start(instance)
        if instance == self.correct_glass:
            self.ball.opacity = 1
            self.points += 10
            if self.points_show:
                self.points_label.text = f"Points: {self.points}"
        else:
            Clock.schedule_once(lambda dt: Animation(pos_hint={'center_y': 0.4}, duration=0.4).start(instance), 1)
        self.end_turn()

    def rigged_win(self, instance):
        if not self.can_click: return
        self.can_click = False
        self.ball.pos_hint = {'center_x': instance.pos_hint['center_x'], 'center_y': 0.4}
        self.ball.opacity = 1
        Animation(pos_hint={'center_y': 0.55}, duration=0.4).start(instance)
        self.points += 10
        self.points_label.text = f"Points: {self.points}"
        self.end_turn()

    def rig_lose(self, instance):
        if not self.can_click: return
        self.can_click = False
        other_glasses = [g for g in self.glasses if g != instance]
        wrong_glass = random.choice(other_glasses)
        self.ball.pos_hint = {'center_x': wrong_glass.pos_hint['center_x'], 'center_y': 0.4}
        
        Animation(pos_hint={'center_y': 0.55}, duration=0.4).start(instance)
        Clock.schedule_once(lambda dt: Animation(pos_hint={'center_y': 0.4}, duration=0.4).start(instance), 1)
        self.points -= 10
        self.points_label.text = f"Points: {self.points}"
        self.end_turn()

class GlassApp(App):
    def build(self):
        return ShufflingGame(level=1, rigged=None, speed=0.5, no_of_glasses=3)

if __name__ == '__main__':
    GlassApp().run()
