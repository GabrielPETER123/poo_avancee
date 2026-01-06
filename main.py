# main.py
import time
import pygame as pg
import pygame_widgets as pw
from renderer import init_renderer
import global_variable as gv
import game
import ui
import utils

def main():
    #** Create Window
    pg.init()
    init_renderer()

    utils.load_game()
    
    clock = pg.time.Clock()
    delta_time: float = 0.0166667

    ui.create_main_menu_widgets()
    ui.create_options_menu_widgets()
    ui.create_upgrade_menu_widgets()

    while gv.running:
        frame_begin_time = time.perf_counter()
        
        #** Get Events
        events = pg.event.get()
        match gv.current_gamemode:    
            case gv.Gamemode.GM_MENU:
                for event in events:
                    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                        gv.running = False
            case gv.Gamemode.GM_GAMEPLAY:
                for event in events:
                    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        gv.change_gamemode(gv.Gamemode.GM_OPTION_MENU)
            case gv.Gamemode.GM_OPTION_MENU:
                for event in events:
                    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        gv.change_gamemode(gv.past_gamemode)
            case gv.Gamemode.GM_UPGRADE_MENU:
                for event in events:
                    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        gv.change_gamemode(gv.Gamemode.GM_MENU)
            
            
        #** Simulate
        game.simulate_game(events, delta_time)
        pw.update(events)
        pg.display.flip()
        
        frame_end_time = time.perf_counter()
        delta_time = frame_end_time - frame_begin_time
        frame_begin_time = frame_end_time
        # Don't Lock Framerate it break calculation of player movement
        clock.tick()
    
    utils.save_game()
    pg.quit()

if __name__ == '__main__':
    main()