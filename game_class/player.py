# player.py
import renderer
import global_variable as gv

class Player:    
    dp_x: float = 0.0
    dp_y: float = 0.0
    ddp_x: float = 0.0
    ddp_y: float = 0.0
    
    # Physics constants
    ddp_x_max: float = 1300.0
    ddp_y_max: float = 1300.0
    ddp_x_min: float = -1300.0
    ddp_y_min: float = -1300.0
        
    def __init__(self, p_x: float = 50.0, p_y: float = 50.0, size: float = 10.0):
        self.p_x = p_x
        self.p_y = p_y
        self.size = size
        
    def aabb_vs_aabb(self, other_x: float, other_y: float, other_size: float):
        return (self.p_x < other_x + other_size and
            self.p_x + self.size > other_x and
            self.p_y < other_y + other_size and
            self.p_y + self.size > other_y)
    
    def simulate_player(self, dt: float):
        # apply acceleration to velocity
        self.dp_x += self.ddp_x * dt
        self.dp_y += self.ddp_y * dt

        # simple drag while accelerating and stronger friction when no input
        drag = 3.0
        friction = 2000.0
        if self.ddp_x == 0.0:
            if self.dp_x > 0.0:
                self.dp_x -= min(self.dp_x, friction * dt)
            elif self.dp_x < 0.0:
                self.dp_x += min(-self.dp_x, friction * dt)
        else:
            self.dp_x -= self.dp_x * drag * dt

        if self.ddp_y == 0.0:
            if self.dp_y > 0.0:
                self.dp_y -= min(self.dp_y, friction * dt)
            elif self.dp_y < 0.0:
                self.dp_y += min(-self.dp_y, friction * dt)
        else:
            self.dp_y -= self.dp_y * drag * dt

        # clamp velocity to a reasonable max speed
        if self.dp_x > gv.player_max_speed: self.dp_x = gv.player_max_speed
        if self.dp_x < -gv.player_max_speed: self.dp_x = -gv.player_max_speed
        if self.dp_y > gv.player_max_speed: self.dp_y = gv.player_max_speed
        if self.dp_y < -gv.player_max_speed: self.dp_y = -gv.player_max_speed

        # integrate position
        self.p_x += self.dp_x * dt
        self.p_y += self.dp_y * dt

        current_offset = renderer.offset_map
        current_width = gv.map_width
        current_height = gv.map_height

        # collisions with map bounds
        if (self.p_x < current_offset):
            self.p_x = current_offset
            self.dp_x = 0.0
        if (self.p_x + self.size > current_width + current_offset):
            self.p_x = current_width + current_offset - self.size
            self.dp_x = 0.0

        if (self.p_y < current_offset):
            self.p_y = current_offset
            self.dp_y = 0.0
        if (self.p_y + self.size > current_height + current_offset):
            self.p_y = current_height + current_offset - self.size
            self.dp_y = 0.0