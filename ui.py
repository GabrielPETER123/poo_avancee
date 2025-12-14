# ui.py
from pygame_widgets.button import Button
from game_class.upgrade import *
import renderer
import global_variable as gv
from const import *

#** Global Variables

# Main Menu
play_button: Button = None
options_button_main: Button = None
quit_button_main: Button = None

# Option Menu
resume_button: Button = None
main_menu_button_options: Button = None
upgrade_menu_button_options: Button = None
quit_button_options: Button = None

# Upgrade Menu
play_button_upgrade_menu: Button = None

main_menu_buttons: list[Button] = []
options_buttons: list[Button] = []
upgrade_buttons: list[Button] = []

button_offset: int = 100
button_width: int = 200
button_height: int = 80
button_x: int = 0
button_y: int = 0

font_size: int = 20


def quit_game():
    # CORRECTION: Used '=' instead of '=='
    gv.running = False

def create_main_menu_widgets():
    """Create widgets once after renderer.init_renderer() has been called."""
    global play_button, options_button_main, quit_button_main, button_offset, button_width, button_height, button_x, button_y, main_menu_buttons
    
    button_x = renderer.half_size_screen_width - (button_width / 2)
    button_y = renderer.half_size_screen_height - (button_height / 2)
    
    play_button_x = options_button_main_x = quit_button_main_x = button_x 
    play_button_y = options_button_main_y = button_y
    quit_button_main_y = renderer.screen_height - button_height
    
    if renderer.game_screen is None:
        raise RuntimeError("create_widgets() must be called after init_renderer()")

    play_button = Button(
        renderer.game_screen,
        play_button_x, play_button_y, button_width, button_height,
        text='Play', fontSize=font_size, margin=20,
        inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0), pressedColour=(0, 200, 20), radius=20,
        onClick=lambda: gv.change_gamemode(gv.Gamemode.GM_GAMEPLAY)
    )
    
    options_button_main = Button(
        renderer.game_screen,
        options_button_main_x, options_button_main_y + button_offset, button_width, button_height,
        text='Options', fontSize=font_size, margin=20,
        inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0), pressedColour=(0, 200, 20), radius=20,
        onClick=lambda: gv.change_gamemode(gv.Gamemode.GM_OPTION_MENU)
    )
    
    quit_button_main = Button(
        renderer.game_screen,
        quit_button_main_x, quit_button_main_y, button_width, button_height,
        text='Quit', fontSize=font_size, margin=20,
        inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0), pressedColour=(0, 200, 20), radius=20,
        onClick=quit_game
    )
    
    main_menu_buttons = [play_button, options_button_main, quit_button_main]

def create_options_menu_widgets():
    global resume_button, main_menu_button_options, upgrade_menu_button_options, quit_button_options, button_offset, button_width, button_height, button_x, button_y, options_buttons, font_size
    button_x = renderer.half_size_screen_width - (button_width / 2)
    button_y = renderer.half_size_screen_height - (button_height / 2)
    
    resume_button_x = main_menu_button_options_x = quit_button_options_x = button_x
    resume_button_y = main_menu_button_options_y = button_y
    quit_button_options_y = renderer.screen_height - button_height
    
    if renderer.game_screen is None:
        raise RuntimeError("create_widgets() must be called after init_renderer()")

    resume_button = Button(
        renderer.game_screen,
        resume_button_x, resume_button_y, button_width, button_height,
        text='Resume', fontSize=font_size, margin=20,
        inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0), pressedColour=(0, 200, 20), radius=20,
        onClick=lambda: gv.change_gamemode(gv.past_gamemode)
    )
    
    main_menu_button_options = Button(
        renderer.game_screen,
        main_menu_button_options_x, main_menu_button_options_y, button_width, button_height,
        text='Main Menu', fontSize=font_size, margin=20,
        inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0), pressedColour=(0, 200, 20), radius=20,
        onClick=lambda: gv.change_gamemode(gv.Gamemode.GM_MENU)
    )
    
    quit_button_options = Button(
        renderer.game_screen,
        quit_button_options_x, quit_button_options_y - button_height, button_width, button_height,
        text='Quit Game', fontSize=font_size, margin=20,
        inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0), pressedColour=(0, 200, 20), radius=20,
        onClick=quit_game
    )
    
    upgrade_menu_button_options = Button(
        renderer.game_screen,
        button_x, button_y - (button_height + 10) * 2, button_width, button_height,
        text='Upgrade', fontSize=font_size, margin=20,
        inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0), pressedColour=(0, 200, 20), radius=20,
        onClick=lambda: gv.change_gamemode(gv.Gamemode.GM_UPGRADE_MENU)
    )
    
    options_buttons = [resume_button, main_menu_button_options, quit_button_options, upgrade_menu_button_options]

def create_game_widgets():
    pass

def create_upgrade_menu_widgets():
    global upgrade_buttons, font_size
    upgrade_buttons.clear()
    for upgrade in UPGRADES:
        upgrade_buttons.append(Button(
            renderer.game_screen,
            (UPGRADE_SIZE + gv.upgrade_button_offset) * UPGRADES.index(upgrade), 0.0, UPGRADE_SIZE, UPGRADE_SIZE,
            text=upgrade.name, fontSize=font_size, margin=20,
            inactiveColour=(upgrade.color), hoverColour=(150, 0, 0), pressedColour=(0, 200, 20), radius=20,
            # capture the current upgrade so each button selects its own
            onClick=lambda u=upgrade: gv.select_upgrade(u)
        ))
    
    # Play Button
    upgrade_buttons.append(Button(
       renderer.game_screen,
        200 + UPGRADE_SIZE + gv.upgrade_button_offset, 200, UPGRADE_SIZE, UPGRADE_SIZE,
        text="Play", fontSize=font_size, margin=20,
        inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0), pressedColour=(0, 200, 20), radius=20,
        onClick=lambda: (gv.change_gamemode(gv.Gamemode.GM_GAMEPLAY), gv.reset_upgrade_selected())
    ))
    
    # Quit Button
    upgrade_buttons.append(Button(
        renderer.game_screen,
        200, 200, UPGRADE_SIZE, UPGRADE_SIZE,
        text="Quit Game", fontSize=font_size, margin=20,
        inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0), pressedColour=(0, 200, 20), radius=20,
        onClick=quit_game
    ))
    
            
def draw_main_menu_widgets(events):
    global main_menu_buttons, options_buttons, upgrade_buttons
    visibility_buttons(False, options_buttons)
    visibility_buttons(False, upgrade_buttons)
    visibility_buttons(False, [gv.buy_button])

    if any(button is None for button in main_menu_buttons):
        return

    for btn in main_menu_buttons:
            btn.draw()
    visibility_buttons(True, main_menu_buttons)

def draw_options_menu_widgets(events):
    global main_menu_buttons, options_buttons, upgrade_buttons
    visibility_buttons(False, main_menu_buttons)
    visibility_buttons(False, upgrade_buttons)
    visibility_buttons(False, [gv.buy_button])

    if any(button is None for button in options_buttons):
        return

    for btn in options_buttons:
        if (btn == main_menu_button_options and gv.past_gamemode == gv.Gamemode.GM_MENU):
            continue
        btn.draw()
                    
    visibility_buttons(True, options_buttons)

def draw_game_widgets(events):
    global main_menu_buttons, options_buttons, upgrade_buttons
    visibility_buttons(False, main_menu_buttons)
    visibility_buttons(False, options_buttons)
    visibility_buttons(False, upgrade_buttons)
    visibility_buttons(False, [gv.buy_button])

def draw_upgrade_menu_widgets(events):
    global main_menu_buttons, options_buttons, upgrade_buttons
    visibility_buttons(False, main_menu_buttons)
    visibility_buttons(False, options_buttons)
    
    if any(button is None for button in upgrade_buttons):
        return
    
    for btn in upgrade_buttons:
        btn.draw()
        
    if gv.upgrade_selected != None:
        gv.buy_button = Button(
            renderer.game_screen,
            renderer.screen_width * 2.5 / 3 - UPGRADE_SIZE / 2 , renderer.screen_height - UPGRADE_SIZE, UPGRADE_SIZE, UPGRADE_SIZE,
            text=f"Buy for {gv.upgrade_selected.cost:.2f} points", fontSize=font_size, margin=20,
            inactiveColour=(LIGHT_GRAY), hoverColour=(150, 0, 0), pressedColour=(0, 200, 20), radius=20,
            onClick=gv.buy_upgrade
        )
        renderer.draw_upgrade_description(gv.upgrade_selected)
        gv.buy_button.draw()
        gv.buy_button.show()        
        gv.buy_button.enable()
        
    visibility_buttons(True, upgrade_buttons)

def visibility_buttons(visibility: bool, buttons: list[Button]):
    for btn in buttons:
        if btn is None:
            return
        if visibility:
            if not btn.isVisible(): btn.show()
            if not btn.isEnabled(): btn.enable()
        else:
            if btn.isVisible(): btn.hide()
            if btn.isEnabled(): btn.disable()