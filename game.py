# game.py
import pygame as pg
import renderer
import ui
from const import *
import random
import global_variable as gv
import time
import math

# ------------------------------------------------------------------
# Map properties
map = 0
offset_map: float = renderer.offset_map

# Player Properties
player_p_x, player_p_y = 0.0, 0.0
reset_player: bool = False

# Timer Variables
timer_temp: float = 0.0
timer: float = 0.0

from game_class.player import Player
from game_class.ball import Ball, Blue_Ball, Yellow_Ball, Green_Ball, Red_Ball

# Instantiate Player and Ball List
player: Player = None 
ball_list: list[Ball] = []


def manage_ball_list():
    global ball_list
    # TODO: Mettre seulement des balles disponibles
    if (len(ball_list) < gv.max_balls_on_screen):
        for _ in range(gv.max_balls_on_screen - len(ball_list)):
            x = random.uniform(offset_map, max(offset_map, gv.map_width + offset_map - gv.ball_size))
            y = random.uniform(offset_map, max(offset_map, gv.map_height + offset_map - gv.ball_size))
            
            ball_type = random.randint(0,3)
            if ball_type == 0:
                ball_list.append(Blue_Ball(x, y, gv.ball_size, gv.blue_ball_value))
            elif ball_type == 1:
                ball_list.append(Yellow_Ball(x, y, gv.yellow_ball_size, gv.yellow_ball_value))
            elif ball_type == 2:
                ball_list.append(Green_Ball(x, y, gv.green_ball_size, gv.green_ball_value))
            elif ball_type == 3:
                ball_list.append(Red_Ball(x, y, gv.red_ball_size, gv.red_ball_value))

def calculate_time():
    global timer, timer_temp
    now = time.perf_counter()
    if (timer_temp == 0.0):
        timer_temp = now
        timer = 0.0
    else:
        timer += now - timer_temp
        timer_temp = now
def render_balls(ball_list: list[Ball]):
    manage_ball_list()
    
    # Render Balls
    for ball in ball_list:
        renderer.draw_ball(ball.color, ball.p_x, ball.p_y, ball.size)

def simulate_balls(player: Player):
    global ball_list
    render_balls(ball_list)
    
    for ball in ball_list:
        if (player.aabb_vs_aabb(ball.p_x, ball.p_y, ball.size)):
            ball.add_point()
            ball_list.remove(ball)
                   
def reset_game():
    global timer, timer_temp, ball_list, player
    player = None
    ball_list = []
    timer_temp = 0.0
    timer = 0.0  
    
def simulate_game(events, dt: float):
    global player, timer, instance_player, player_p_x, player_p_y, reset_player, reseting_game

    if reset_player:
        player = None
        reset_player = False
    
    if player == None:
        player_p_x, player_p_y = (gv.map_width - gv.player_size) * .5 + offset_map, (gv.map_height - gv.player_size) * .5 + offset_map
        player = Player(player_p_x, player_p_y, gv.player_size)
        instance_player = False
         
    match gv.current_gamemode:
        case gv.Gamemode.GM_MENU:
            reset_game()
            draw_main_menu(events)
        case gv.Gamemode.GM_GAMEPLAY:
            # keep iterating events so other systems can react
            for event in events:
                pass
            
            # read continuous key state
            keys = pg.key.get_pressed()
            acc = 1200.0
            if keys[pg.K_z]:
                player.ddp_y = -acc
            elif keys[pg.K_s]:
                player.ddp_y = acc
            else:
                player.ddp_y = 0.0

            if keys[pg.K_d]:
                player.ddp_x = acc
            elif keys[pg.K_q]:
                player.ddp_x = -acc
            else:
                player.ddp_x = 0.0

            # clamp accelerations to configured min/max
            if player.ddp_x > player.ddp_x_max: player.ddp_x = player.ddp_x_max
            if player.ddp_x < player.ddp_x_min: player.ddp_x = player.ddp_x_min
            if player.ddp_y > player.ddp_y_max: player.ddp_y = player.ddp_y_max
            if player.ddp_y < player.ddp_y_min: player.ddp_y = player.ddp_y_min

            player.simulate_player(dt)
            draw_gameplay(events)
            simulate_balls(player)
            calculate_time()
            # TODO: Mettre le message de changement de screen pour aller sur les upgrades ou restart une game
            if (timer > gv.round_time):
                reset_game()
                gv.change_gamemode(gv.Gamemode.GM_UPGRADE_MENU)

        case gv.Gamemode.GM_OPTION_MENU:
            draw_options_menu(events)    
        case gv.Gamemode.GM_UPGRADE_MENU:
            reset_player = True
            reset_game()
            draw_upgrade_menu(events)

def draw_main_menu(events):
    renderer.clear_screen(0x344444)
    ui.draw_main_menu_widgets(events)

def draw_options_menu(events):
    renderer.clear_screen(0xAAAAAA)
    ui.draw_options_menu_widgets(events)

def draw_gameplay(events):
    global player, timer, round_time
    p_x = 0.0
    p_y = 0.0
    text = ""
    renderer.clear_screen(BLUE)
    ui.draw_game_widgets(events)
    renderer.draw_map(map)
    renderer.draw_player(player.p_x, player.p_y, player.size)
    
    # Draw Time Left
    p_x = renderer.screen_width - gv.map_width * 0.2
    p_y = renderer.screen_height * 0.1
    if (gv.round_time - timer > 0.0):
        text = "Time Left: " + str(math.ceil(gv.round_time - timer)) + "s"
    else:
        text = "No Time Left"
    
    renderer.draw_text(text, WHITE, p_x, p_y)
    
    # Draw Player Score
    p_x = renderer.screen_width - gv.map_width * 0.2
    p_y = renderer.screen_height * 0.2
    text = f"Points: {gv.points:.2f}"
    renderer.draw_text(text, WHITE, p_x, p_y)
    
def draw_upgrade_menu(events):
    renderer.clear_screen(GRAY)
    renderer.draw_uprgrade_menu()
    ui.draw_upgrade_menu_widgets(events)