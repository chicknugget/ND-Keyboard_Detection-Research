from shuffle import ShufflingGame
from kivy.app import App
from datetime import datetime 

class BaseGame(App):
    class RelaxationGame(App): #Level 1, practice round, no points, no pressure, simple shuffle, low speed
        def build(self):
            return ShufflingGame(level=1, rigged=None, speed=0.65, no_of_glasses=3, points_show = False, total_rounds=7)
        
        def on_start(self):
            self.start_time = datetime.now()
            print(self.start_time)
        
        def on_stop(self):
            self.end_time = datetime.now()
            print(self.end_time)

    class HappyGame(App): #Level 2, easy round, some points, low pressure, simple shuffle, medium speed, rigged
        def build(self):
            return ShufflingGame(level=2, rigged="rig_win", speed=0.5, no_of_glasses=3, points_show = True)
        
        def on_start(self):
            self.start_time = datetime.now()
            print(self.start_time)
        
        def on_stop(self):
            self.end_time = datetime.now()
            print(self.end_time)

    class BoredomGame(App): #Level 3, one glass, simple points, no shuffle, medium speed
        def build(self):
            return ShufflingGame(level=3, rigged=None, speed=0.5, no_of_glasses=1, points_show = True, total_rounds=3)
        
        def on_start(self):
            self.start_time = datetime.now()
            print(self.start_time)
        
        def on_stop(self):
            self.end_time = datetime.now()
            print(self.end_time)

    class SadGame(App): #Level 4, 9 wins 1 loss, rigged
        def build(self):
            return ShufflingGame(level=4, rigged="rig_nwin_oloss", speed=0.5, no_of_glasses=4, points_show=True, total_rounds=5)
        
        def on_start(self):
            self.start_time = datetime.now()
            print(self.start_time)
        
        def on_stop(self):
            self.end_time = datetime.now()
            print(self.end_time)
        
    class FrustratedGame(App): #Level 5, 1 random win 9 losses, rigged
        def build(self):
            return ShufflingGame(level=5, rigged="rig_owin_nloss", speed=0.4, no_of_glasses=5, points_show = True)
        
        def on_start(self):
            self.start_time = datetime.now()
            print(self.start_time)
        
        def on_stop(self):
            self.end_time = datetime.now()
            print(self.end_time)

    class StressGame(App): #Level 6, all losses, losing points, hard round, high points, high pressure, complex shuffle, high speed, rigged
        def build(self):
            return ShufflingGame(level=6, rigged="rig_lose", speed=0.35, no_of_glasses=6, points_show = True)
        
        def on_start(self):
            self.start_time = datetime.now()
            print(self.start_time)
        
        def on_stop(self):
            self.end_time = datetime.now()
            print(self.end_time)

if __name__ == '__main__':
    x= int(input("Enter Number:"))
    if x==1:
        BaseGame().RelaxationGame().run()
    elif x==2:
        BaseGame().HappyGame().run()
    elif x==3:
        BaseGame().BoredomGame().run()
    elif x==4:
        BaseGame().SadGame().run()
    elif x==5:
        BaseGame().FrustratedGame().run()
    elif x==6:
        BaseGame().StressGame().run()