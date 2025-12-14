# upgrade.py
from enum import Enum
import global_variable as gv
from const import *

class Upgrade_Type(Enum):
    BALL_SIZE = 0
    BALL_VALUE = 1
    BALL_ON_SCREEN = 2
    PLAYER_SIZE = 3
    PLAYER_SPEED = 4
    TIME = 5

# ---------------UPGRADE CLASS---------------*
# ? RED: TIME, BLUE: PLAYER, WHITE: BALL
class Upgrade:
    remaining_level: int = 0
    def __init__(self, name: str, cost: float, type: Upgrade_Type, value: float, max_level: int, color: int):
        self.name = name
        self.cost = cost
        self.type = type
        self.value = value
        self.max_level = max_level
        self.color = color
        self.remaining_level = self.max_level
    
    def upgrade(self):
        if self.remaining_level <= 0 or gv.points < self.cost:
            return
        self.remaining_level -= 1
        gv.points -= self.cost
        self.cost *= 1.2

        match self.type:
            case Upgrade_Type.BALL_SIZE:
                gv.ball_size *= 1 + (self.value / 100.0)
                gv.init_ball_sizes()
            case Upgrade_Type.BALL_VALUE:
                gv.ball_value += self.value
                gv.init_ball_values()
            case Upgrade_Type.BALL_ON_SCREEN:
                gv.max_balls_on_screen += self.value
            case Upgrade_Type.PLAYER_SIZE:
                gv.player_size *= 1 + (self.value / 100.0)
            case Upgrade_Type.PLAYER_SPEED:
                gv.player_max_speed += self.value
            case Upgrade_Type.TIME:
                gv.round_time += self.value

# ---------------UPGRADES---------------
UPGRADES: list[Upgrade] = [
    Upgrade("Player Size", 10.0, Upgrade_Type.PLAYER_SIZE, 10.0, 5, BLUE),
    Upgrade("Player Speed", 10.0, Upgrade_Type.PLAYER_SPEED, 150.0, 5, BLUE),
    Upgrade("Maximum Balls", 5.0,  Upgrade_Type.BALL_ON_SCREEN, 1, 10, WHITE),
    Upgrade("Ball Size", 10.0, Upgrade_Type.BALL_SIZE, 10.0, 3, WHITE),
    Upgrade("Ball Value", 15.0, Upgrade_Type.BALL_VALUE, 10.0, 5, WHITE),
    Upgrade("Round Time", 20.0, Upgrade_Type.TIME, 2, 5, RED)
]
