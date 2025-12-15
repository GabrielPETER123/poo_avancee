# ball.py
from const import *
from game_class.player import Player
import global_variable as gv

# ---------------BALL CLASS---------------
class Ball:
    color: int = 0

    def __init__(self, p_x: float, p_y: float, size: float, value: float):
        self.p_x = p_x
        self.p_y = p_y
        self.size = size
        self.value = value
        
    def add_point(self):
        gv.points += self.value
        
class Blue_Ball(Ball):
    color: int = BLUE

    def __init__(self, p_x, p_y, size, value):
        super().__init__(p_x, p_y, size, value)

class Yellow_Ball(Ball):
    color: int = YELLOW

    def __init__(self, p_x, p_y, size, value):
        super().__init__(p_x, p_y, size, value)
               
class Green_Ball(Ball):
    color: int = GREEN

    def __init__(self, p_x, p_y, size, value):
        super().__init__(p_x, p_y, size, value)
             
class Red_Ball(Ball):
    color: int = RED
    damage: float = 10.0

    def __init__(self, p_x, p_y, size, value):
        super().__init__(p_x, p_y, size, value)
       
    def damage_player(self, player: Player):
        if player.health > self.damage:
            player.health -= self.damage         
        else: gv.end_round = True