# renderer.py
import pygame as pg
from utils import *
import global_variable as gv
from const import *
from game_class.upgrade import Upgrade, Upgrade_Type

#** Global Variables
game_screen = None
screen_width: int = 0
screen_height: int = 0
half_size_screen_width: int = 0
half_size_screen_height: int = 0
offset_map: float = 50.0
font = None 


def init_renderer(size=None, fullscreen=False):
    global game_screen, screen_width, screen_height, half_size_screen_width, half_size_screen_height, offset_map, font
    # Ensure the display module is initialized before querying or using mouse/display APIs.
    if not pg.display.get_init():
        pg.display.init()
    if not pg.font.get_init():
        pg.font.init()
        font = pg.font.Font(pg.font.get_default_font(), 36)
    
    

    if size is None:
        info = pg.display.Info()
        screen_width, screen_height = info.current_w, info.current_h
        half_size_screen_width, half_size_screen_height = screen_width // 2, screen_height // 2
        gv.map_width = (screen_width - offset_map * 2) * 0.8
        gv.map_height = screen_height - offset_map * 2
    else:
        screen_width, screen_height = size

    flags = 0
    if fullscreen:
        flags = pg.FULLSCREEN

    game_screen = pg.display.set_mode((screen_width, screen_height), flags)
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
        font = pg.font.Font(pg.font.get_default_font(), 36)
    if isinstance(color, int):
        color = ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)

    # Handle multi-line strings manually
    lines = text.split("\n")
    lh = line_height or font.get_linesize()
    for i, line in enumerate(lines):
        surface = font.render(line, True, color)
        game_screen.blit(surface, dest=(p_x, p_y + i * lh))


def draw_uprgrade_menu():
    global game_screen, screen_width, screen_height
    
    game_screen.fill(DARK_GRAY, pg.Rect(screen_width * 2 / 3, 0.0, screen_width, screen_width))
    text = f"Points: {gv.points:.2f}"
    draw_text(text, BLUE, screen_width *2 / 3, screen_height / 2)
    
def draw_upgrade_description(upgrade: Upgrade):
    description: str = ""
    match upgrade.type:
        case Upgrade_Type.PLAYER_SIZE:
            description = "Increase Player Size by 10px"
        case Upgrade_Type.PLAYER_SPEED:
            description = "Increase Player Max Acceleration \nby 150"
        case Upgrade_Type.BALL_ON_SCREEN:
            description = "Increase the number of ball \nthat can spawn by 1"
        case Upgrade_Type.BALL_SIZE:
            description = "Increase Ball Size by 10px"
        case Upgrade_Type.BALL_VALUE:
            description = "Rise the value of balls by 10 points"
        case Upgrade_Type.TIME:
            description = "Increase the time you can play\nby 2s"
            
    draw_text(description, WHITE, screen_width * 2 / 3, 0.0)

def draw_map(id: int):
    global offset_map
    if game_screen is None:
        raise RuntimeError("renderer.init_renderer() must be called before drawing")

    match id:
        case 0:
            rects = [ 
                {
                    'color': 0x444455,
                    'rect': pg.Rect(offset_map, offset_map, gv.map_width, gv.map_height)
                }
            ]
            for rect in rects:
                color = rect['color']
                if isinstance(color, int):
                    color = ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)
                game_screen.fill(color, rect['rect'])

