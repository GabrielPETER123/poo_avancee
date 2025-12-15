# renderer.py
import pygame as pg
import global_variable as gv
from const import *
from game_class.upgrade import Upgrade, Upgrade_Type

#** Global Variables
game_screen = None
half_size_screen_width: float = .0
half_size_screen_height: float = .0
font = None 


def init_renderer(size=None, fullscreen=False):
    global game_screen, half_size_screen_width, half_size_screen_height, font
    if not pg.display.get_init():
        pg.display.init()
    if not pg.font.get_init():
        pg.font.init()
        font = pg.font.Font(pg.font.get_default_font(), 36)

    if size is None:
        info = pg.display.Info()
        gv.screen_width, gv.screen_height = info.current_w, info.current_h
    else:
        gv.screen_width, gv.screen_height = size

    gv.offset_map_width, gv.offset_map_height = gv.screen_width * .1, gv.screen_height * .1
    half_size_screen_width, half_size_screen_height = gv.screen_width // 2, gv.screen_height // 2
    gv.map_width = (gv.screen_width - gv.offset_map_width * 2) * .8
    gv.map_height = gv.screen_height - gv.offset_map_height * 2

    gv.player_size = gv.screen_width * .05
    gv.ball_size = gv.screen_width * .01
    gv.init_ball_sizes()
    gv.init_ball_values()

    gv.button_offset = gv.screen_height * .05
    gv.button_width = gv.screen_width * .1
    gv.button_height = gv.screen_height * .07

    gv.upgrade_size = gv.screen_height * .125
    gv.upgrade_button_offset = gv.screen_width * .01

    flags = 0
    if fullscreen:
        flags = pg.FULLSCREEN

    game_screen = pg.display.set_mode((gv.screen_width, gv.screen_height), flags)
    pg.display.set_caption("INCREMENTAL GAME")

def clear_screen(color=0x444a46):
    if game_screen is None:
        raise RuntimeError("renderer.init_renderer() must be called before drawing")

    if isinstance(color, int):
        # convert 0xRRGGBB to (r,g,b)
        color = ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)
    game_screen.fill(color)


def draw_options():
    pass

def draw_player(p_x, p_y, size):
    if game_screen is None:
        raise RuntimeError("renderer.init_renderer() must be called before drawing")
    try:
        color = (255, 255, 255)
        game_screen.fill(color, pg.Rect(p_x, p_y, size, size))
    except Exception:
        return
    
def draw_ball(color, p_x, p_y, size):
    if game_screen is None:
        raise RuntimeError("renderer.init_renderer() must be called before drawing")
    try:
        # convert color int to tuple if needed
        if isinstance(color, int):
            color = ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)
        game_screen.fill(color, pg.Rect(p_x, p_y, size, size))
    except Exception:
        return
    
def draw_text(text: str, color: tuple, p_x, p_y, line_height: int | None = None):
    """Draw text; supports explicit newlines by rendering line-by-line."""
    global font
    if game_screen is None:
        raise RuntimeError("renderer.init_renderer() must be called before drawing")
    if font is None:
        if not pg.font.get_init():
            pg.font.init()
        font = pg.font.Font(pg.font.get_default_font(), 30)
    if isinstance(color, int):
        color = ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)

    # Handle multi-line strings manually
    lines = text.split("\n")
    lh = line_height or font.get_linesize()
    for i, line in enumerate(lines):
        surface = font.render(line, True, color)
        game_screen.blit(surface, dest=(p_x, p_y + i * lh))


def draw_uprgrade_menu():
    global game_screen
    
    game_screen.fill(DARK_GRAY, pg.Rect(gv.screen_width * 2 / 3, 0.0, gv.screen_width, gv.screen_width))
    text = f"Points: {gv.points:.2f}"
    draw_text(text, BLUE, gv.screen_width *2 / 3, gv.screen_height / 2)
    
def draw_upgrade_description(upgrade: Upgrade):
    description: str = ""
    match upgrade.type:
        case Upgrade_Type.PLAYER_SIZE:
            description = "Increase Player Size by 10%"
        case Upgrade_Type.PLAYER_SPEED:
            description = "Increase Player Max Acceleration \nby 150"
        case Upgrade_Type.PLAYER_HEALTH:
            description = "Increase Player Health by 7.5"
        case Upgrade_Type.BALL_ON_SCREEN:
            description = "Increase the number of ball \nthat can spawn by 1"
        case Upgrade_Type.BALL_SIZE:
            description = "Increase Ball Size by 10%"
        case Upgrade_Type.BALL_VALUE:
            description = "Rise the value of balls by 10 points"
        case Upgrade_Type.TIME:
            description = "Increase the time you can play\nby 2s"
    draw_text(description, WHITE, gv.screen_width * 2 / 3, 0.0)
    draw_text(f"Level {upgrade.max_level - upgrade.remaining_level} / {upgrade.max_level}", WHITE, gv.screen_width * 2 / 3, gv.screen_height / 3)

def draw_map(id: int):
    if game_screen is None:
        raise RuntimeError("renderer.init_renderer() must be called before drawing")

    match id:
        case 0:
            rects = [ 
                {
                    'color': 0x444455,
                    'rect': pg.Rect(gv.offset_map_width, gv.offset_map_height, gv.map_width, gv.map_height)
                }
            ]
            for rect in rects:
                color = rect['color']
                if isinstance(color, int):
                    color = ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)
                game_screen.fill(color, rect['rect'])

