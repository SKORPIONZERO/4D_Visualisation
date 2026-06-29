"""
app.py
 
App owns the pygame window, the clock, and the main loop. It holds
the states that change frame to frame (theta, whether rotation is
currently playing, whether w-values are shown) as instance attributes
"""
import pygame
import math
import polytopes
import config

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("4D Object Rotation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        
        self.running = True
        self.w_values_enabled = True
        self.rotation_speed = config.BASE_ROTATION_SPEED
        
        self.order_rotation_applied = config.PLANES
        self.angles = {plane: 0.0 for plane in config.PLANES}
        self.auto_rotation = {plane: False for plane in config.PLANES}
        self.rotation_speeds = {plane: self.rotation_speed for plane in config.PLANES}
        self.chosen_plane = config.PLANES[0]

        self.polytope = polytopes.Tesseract()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.auto_rotation[self.chosen_plane] = not self.auto_rotation[self.chosen_plane]
                if event.key == pygame.K_t:
                    self.w_values_enabled = not self.w_values_enabled
                for key, plane in config.PLANE_KEYS.items():
                    if event.key == key:
                        self.chosen_plane = plane
                # TODO: Add more event handling as needed (e.g., for rotation speed adjustment, changing objects)
    
    def update(self):
        for plane in config.PLANES:
            if self.auto_rotation[plane]:
                self.angles[plane] = (self.angles[plane] + self.rotation_speed) % (2 * math.pi)
        # TODO: Add logic for calculating vertices, edges, and colors based on the current theta and other parameters.
    
    def render(self):
        self.screen.fill(config.BACKGROUND)
        # TODO: Add rendering logic for the 4D object, including drawing vertices, edges, and optionally displaying w-values.
        pygame.display.update()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(config.FPS)
        pygame.quit()
