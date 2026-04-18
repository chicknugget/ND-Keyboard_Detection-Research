

from kivy.app import App
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty
from kivy.core.audio import SoundLoader
import random
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_PATH = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

random_win = random.randint(1, 4)
 
class ImageButton(ButtonBehavior, Image):
    pass

class ShufflingGame(FloatLayout):
    speed = NumericProperty(0.5)
    

    def __init__(self, level = 0, rigged=None, speed=0.5, no_of_glasses=3, points_show=True, total_rounds=10, on_game_complete=None, bg_music=None, **kwargs):
        super(ShufflingGame, self).__init__(**kwargs)

        self.on_game_complete = on_game_complete
        self.level = level
        self.rigged = rigged
        self.speed = speed
        self.no_of_glasses = no_of_glasses
        self.total_rounds = total_rounds
        self.points_show = points_show
        self.total_shuffles = 3
        self.current_round = 1
        self.success_ding = SoundLoader.load(os.path.join(BASE_PATH, 'assets', 'music', 'dings', 'success_ding.wav'))
        self.success_ding.volume = 0.5
        self.lose_ding = SoundLoader.load(os.path.join(BASE_PATH, 'assets', 'music', 'dings', 'lose_ding.wav'))
        self.bg_music = SoundLoader.load(os.path.join(BASE_PATH, 'assets', 'music', 'bg music', f'{bg_music}.mp3')) if bg_music else None
        if self.bg_music:
            self.bg_music.loop = True      
            self.bg_music.volume = 0.1
            self.bg_music.play()
        self.counter = 1
        self.app = App.get_running_app()

        with self.canvas.before:
            Color(97/255, 112/255, 44/255, 1)   
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.level_label = Label(text=f"Level {self.level}:", 
                   font_size='30sp',
                   font_name = os.path.join(BASE_PATH, 'assets', 'fonts', 'PrStart.ttf'),
                   color=(46/255, 34/255, 4/255, 1), 
                   size_hint=(0.8, 0.1), 
                   pos_hint={'center_x': 0.5, 'top': 0.9})
        self.add_widget(self.level_label)

        self.round_label = Label(text=f"Round {self.current_round}:", 
                   font_size='20sp',
                   font_name = os.path.join(BASE_PATH, 'assets', 'fonts', 'PrStart.ttf'),
                   color=(64/255, 48/255, 6/255, 1), 
                   size_hint=(0.8, 0.1), 
                   pos_hint={'center_x': 0.5, 'top': 0.8})
        self.add_widget(self.round_label)

        self.points_label = Label(text=f"Points: {self.app.total_points}", 
                   font_size='10sp',
                   font_name = os.path.join(BASE_PATH, 'assets', 'fonts', 'PrStart.ttf'),
                   color=(64/255, 48/255, 6/255, 1), 
                   size_hint=(0.8, 0.1), 
                   pos_hint={'center_x': 0.5, 'top': 0.75},
                   opacity=1 if self.points_show else 0)
        self.add_widget(self.points_label)

        self.find_ball = Label(text=f"{self.counter}...", 
                   font_size='15sp',
                   font_name = os.path.join(BASE_PATH, 'assets', 'fonts', 'PrStart.ttf'),
                   color=(48/255, 42/255, 3/255, 1),
                   size_hint=(0.6, 0.1),
                   pos_hint={'center_x': 0.5, 'top': 0.7},
                   opacity=0)
        self.add_widget(self.find_ball)

        self.point_change = Label(text = "",
                   font_size='25sp',
                   font_name = os.path.join(BASE_PATH, 'assets', 'fonts', 'PrStart.ttf'),
                   color=(189/255, 141/255, 30/255, 1),
                   size_hint=(0.6, 0.1),
                   opacity=0)
        self.add_widget(self.point_change)

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
            source = os.path.join(BASE_PATH, 'assets', 'cup_ball', 'ball.png'), 
            size_hint=(width_hint*0.6, 0.1), 
            opacity=0,
            pos_hint={'center_x': self.lanes[self.correct_index], 'center_y': 0.4}
        )
        self.add_widget(self.ball)

        for i in range(self.no_of_glasses):
            width_hint = 0.75 / self.no_of_glasses
            btn = ImageButton(
                source = os.path.join(BASE_PATH, 'assets', 'cup_ball', 'cup.png'), 
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
            self.counter = 1
            self.find_ball.text = f"{self.counter}..."
            self.find_ball.opacity = 0
            
            for glass in self.glasses:
                self.remove_widget(glass)
            self.setup_game()
        else:
            if hasattr(self,'next_level_button'):
                return
            
            self.can_click =False
            self.round_label.text ="Game Over"

            #decide button text based on final level
            is_final_game = (self.level ==7)

            self.next_level_button = Button(
                text="Finish Game" if is_final_game else "Next Level",
                size_hint=(0.7, 0.1),
                pos_hint={'center_x': 0.5, 'center_y': 0.2},
                font_size='20sp',
                font_name=os.path.join(BASE_PATH, 'assets', 'fonts', 'PrStart.ttf'),
                background_color=(0.38, 0.26, 0.04, 1),
                color=(232/255, 208/255, 149/255, 1)
            )

            self.next_level_button.bind(on_press=self.finish_game)
            self.add_widget(self.next_level_button)
            if self.bg_music:
                self.bg_music.stop()


    def finish_game(self,instance):
        app = App.get_running_app()
        #counting level completed to print
        completed = app.user_data.setdefault('completed_games',set())
        completed.add(self.level)
        
        if self.on_game_complete:
            self.on_game_complete()

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
        self.find_ball.opacity = 1
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
            self.find_ball.text = f"{self.counter + 1}..."
            self.shuffle_glasses()
        else:
            self.find_ball.text = "Find the ball!"
            self.can_click = True

    def end_turn(self):
        Clock.schedule_once(lambda dt: self.next_round(), 2.0)

    def rig_nwin_oloss(self, instance):
        if self.current_round < self.total_rounds:
            if not self.can_click: return
            self.can_click = False
            self.ball.pos_hint = {'center_x': instance.pos_hint['center_x'], 'center_y': 0.4}
            Animation(pos_hint={'center_y': 0.55}, duration=0.4).start(instance)
            self.winning_glass(instance, instance.pos_hint['center_x'], 0.5)
        else:
            if not self.can_click: return
            self.can_click = False
            other_glasses = [g for g in self.glasses if g != instance]
            wrong_glass = random.choice(other_glasses)
            self.ball.pos_hint = {'center_x': wrong_glass.pos_hint['center_x'], 'center_y': 0.4}
            Animation(pos_hint={'center_y': 0.55}, duration=0.4).start(instance)
            self.losing_glass(instance, instance.pos_hint['center_x'], 0.5)
        self.end_turn()

    def rig_owin_nloss(self, instance, random_win):
        if self.current_round == random_win:
            if not self.can_click: return
            self.can_click = False
            self.ball.pos_hint = {'center_x': instance.pos_hint['center_x'], 'center_y': 0.4}
            Animation(pos_hint={'center_y': 0.55}, duration=0.4).start(instance)
            self.winning_glass(instance, instance.pos_hint['center_x'], 0.5)
        else:
            if not self.can_click: return
            self.can_click = False
            other_glasses = [g for g in self.glasses if g != instance]
            wrong_glass = random.choice(other_glasses)
            self.ball.pos_hint = {'center_x': wrong_glass.pos_hint['center_x'], 'center_y': 0.4}
            Animation(pos_hint={'center_y': 0.55}, duration=0.4).start(instance)
            self.losing_glass(instance, instance.pos_hint['center_x'], 0.5)
        self.end_turn()

    def check_guess(self, instance):
        if not self.can_click: return
        self.can_click = False
        self.ball.pos_hint = {'center_x': self.correct_glass.pos_hint['center_x'], 'center_y': 0.4}
        Animation(pos_hint={'center_y': 0.55}, duration=0.4).start(instance)
        if instance == self.correct_glass:
            self.winning_glass(instance, instance.pos_hint['center_x'], 0.5)
        else:
            Clock.schedule_once(lambda dt: Animation(pos_hint={'center_y': 0.4}, duration=0.4).start(instance), 1)
        self.end_turn()

    def rigged_win(self, instance):
        if not self.can_click: return
        self.can_click = False
        self.ball.pos_hint = {'center_x': instance.pos_hint['center_x'], 'center_y': 0.4}
        Animation(pos_hint={'center_y': 0.55}, duration=0.4).start(instance)
        self.winning_glass(instance, instance.pos_hint['center_x'], 0.5)
        self.end_turn()

    def rig_lose(self, instance):
        if not self.can_click: return
        self.can_click = False
        other_glasses = [g for g in self.glasses if g != instance]
        wrong_glass = random.choice(other_glasses)
        self.ball.pos_hint = {'center_x': wrong_glass.pos_hint['center_x'], 'center_y': 0.4}
        Animation(pos_hint={'center_y': 0.55}, duration=0.4).start(instance)
        self.losing_glass(instance, instance.pos_hint['center_x'], 0.5)
        self.end_turn()

    def winning_glass(self, instance, center_x, center_y):

        if self.success_ding:
            self.success_ding.play()
        
        self.point_change.text = "+10"
        self.point_change.opacity = 1
        self.point_change.pos_hint = {'center_x': center_x, 'center_y': center_y}
        point_anim = Animation(pos_hint={'center_y': 0.6}, 
                                opacity = 0, 
                                duration=0.7,
                                t='out_quad')
        point_anim.start(self.point_change)

        self.ball.opacity = 1
        if self.points_show:
            self.app.total_points += 10
            self.points_label.text = f"Points: {self.app.total_points}"
    
    def losing_glass(self, instance, center_x, center_y):
        if self.lose_ding:
            self.lose_ding.play()

        self.point_change.text = "-10"
        self.point_change.opacity = 1
        self.point_change.pos_hint = {'center_x': center_x, 'center_y': center_y}
        point_anim = Animation(pos_hint={'center_y': 0.4}, 
                                opacity = 0, 
                                duration=0.7,
                                t='out_quad')
        point_anim.start(self.point_change)

        
        Clock.schedule_once(lambda dt: Animation(pos_hint={'center_y': 0.4}, duration=0.4).start(instance), 1)
        self.app.total_points -= 10
        self.points_label.text = f"Points: {self.app.total_points}"


class GlassApp(App):
    def build(self):
        return ShufflingGame(level=1, rigged="rig_nwin_oloss", speed=0.5, total_rounds=5, points_show=True, no_of_glasses=3, bg_music="happy", on_game_complete = lambda : print("game finished"))


if __name__ == '__main__':
    GlassApp().run()
