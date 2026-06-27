"""
app.py
 
App owns the pygame window, the clock, and the main loop. It holds
the states that change frame to frame (theta, whether rotation is
currently playing, whether w-values are shown) as instance attributes
"""
import pygame
import math
from config import WIDTH, HEIGHT, FPS, ROTATION_SPEED, BACKGROUND

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("4D Object Rotation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        
        self.running = True
        self.theta = 0.0
        self.theta_changing = False
        self.w_values_enabled = True
        self.rotation_speed = ROTATION_SPEED
        
        # TODO: Initialize other necessary attributes for the 4D object, vertices, edges, and colors.
        self.polytope = None  # Placeholder for the 4D object (e.g., tesseract)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.theta_changing = not self.theta_changing
                elif event.key == pygame.K_t:
                    self.w_values_enabled = not self.w_values_enabled
                # TODO: Add more event handling as needed (e.g., for rotation speed adjustment, changing objects)
    
    def update(self):
        if self.theta_changing:
            self.theta = (self.theta + self.rotation_speed) % (2 * math.pi)
        # TODO: Add logic for calculating vertices, edges, and colors based on the current theta and other parameters.
    
    def render(self):
        self.screen.fill(BACKGROUND)
        # TODO: Add rendering logic for the 4D object, including drawing vertices, edges, and optionally displaying w-values.
        pygame.display.update()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        pygame.quit()
