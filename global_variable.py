# global_variable.py
from enum import Enum
from game_class.upgrade import Upgrade
from pygame_widgets.button import Button

# Main Loop
running: bool = True

# Gamemode
class Gamemode(Enum):
    GM_MENU = 0
    GM_GAMEPLAY = 1
    GM_OPTION_MENU = 2
    GM_UPGRADE_MENU = 3
    
past_gamemode = None
current_gamemode = Gamemode.GM_MENU

# Game Properties
round_time: float = 10.0
end_round: bool = False

# Screen Properties
screen_width: float = .0
screen_height: float = .0
points: float = .0

# Button Properties
button_offset: float = screen_height * .05
button_width: float = screen_width * .1
button_height: float = screen_height * .07

# Map Properties
offset_map_width: float = .0
offset_map_height: float = .0
map_width: float = .0 
map_height: float = .0

# Player Properties
player_size: float = 50.0
player_max_speed: float = 800.0
player_health: float = 50.0

# Ball Properties
max_balls_on_screen: int = 5
ball_size: float = 10.0
ball_value: float = 10.0
blue_ball_value = yellow_ball_value = green_ball_value = red_ball_value = .0
blue_ball_size = yellow_ball_size = green_ball_size = red_ball_size = .0

# Upgrade Button Properties
upgrade_size: float = .0
upgrade_button_offset: float = .0
upgrade_selected: Upgrade = None

# Buy Button
buy_button: Button = None

def init_ball_sizes():
    global blue_ball_size, yellow_ball_size, green_ball_size, red_ball_size
    blue_ball_size = yellow_ball_size = green_ball_size = red_ball_size = ball_size

def init_ball_values():
    global blue_ball_value, yellow_ball_value, green_ball_value, red_ball_value 
    blue_ball_value = yellow_ball_value = green_ball_value = red_ball_value = ball_value

def change_gamemode(futur_gamemode: Gamemode):
    global past_gamemode, current_gamemode
    past_gamemode, current_gamemode = current_gamemode, futur_gamemode
    
def select_upgrade(upgrade: Upgrade):
    global upgrade_selected
    upgrade_selected = upgrade
    
def buy_upgrade():
    global upgrade_selected
    upgrade_selected.upgrade()

def reset_upgrade_selected():
    global upgrade_selected
    upgrade_selected = None
