class GameVariables:
    def __init__(self):
        self.in_slow_motion_mode = False
        self.in_speed_mode = False
        self.speed_shown = 0
        self.slow_shown = 0 
        self.cucarachas_shown = 0 
        self.spawn_timer = 0
        self.a = 0
        self.b = 0
        self.score = 0

    def reset(self):
        self.in_slow_motion_mode = False
        self.in_speed_mode = False
        self.speed_shown = 0
        self.slow_shown = 0 
        self.cucarachas_shown = 0 
        self.spawn_timer = 0
        self.a = 0
        self.b = 0
        self.score = 0