"""
app.py
 
App owns the pygame window, the clock, and the main loop. It holds
the states that change frame to frame (theta, whether rotation is
currently playing, whether w-values are shown) as instance attributes
"""
import pygame
import math
import numpy as np
import polytopes
import rotation
import projection
import config
import rendering

class App:
    def __init__(self):
        self.display = rendering.Display()
        self.polytope = polytopes.Tesseract()
        
        self.running = True
        self.centre = np.array([self.display.screen.get_width() / 2, self.display.screen.get_height() / 2])
        self.auto_rotation = False
        self.order_rotation_applied = config.PLANES
        self.chosen_plane = config.PLANES[0]
        self.angles = {plane: 0.0 for plane in config.PLANES}
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.polytope = polytopes.Tesseract()
                if event.key == pygame.K_w:
                    self.polytope = polytopes.Cell16()
                if event.key == pygame.K_SPACE:
                    self.auto_rotation = not self.auto_rotation
                if event.key == pygame.K_t:
                    self.display.w_values_enabled = not self.display.w_values_enabled
                if event.key == pygame.K_h:
                    self.display.helper_legend_enabled = not self.display.helper_legend_enabled
                if event.key == pygame.K_TAB:
                    self.display.lerp_mode = (self.display.lerp_mode + 1) % len(config.LERP_MODES)
                for key, plane in config.PLANE_KEYS.items():
                    if event.key == key:
                        self.chosen_plane = plane
                # TODO: Add more event handling as needed (e.g., for rotation speed adjustment, changing objects)
    
    def update(self):
        if self.auto_rotation:
            for plane in config.PLANES:
                self.angles[plane] = (self.angles[plane] + config.ROTATION_SPEED) % (2 * math.pi)
        self.order_rotation_applied = ("zw", "yz", "yw", "xz", "xy", "xw")
        composed_rotation_matrix = rotation.compose_rotation_matrices(self.angles, self.order_rotation_applied)
        projected_vertices, w_values = [], []
        for vertex in self.polytope.vertices:
            projected_vertex, w_value = projection.project_4D_to_2D(composed_rotation_matrix @ vertex, config.DISTANCE_4D, config.DISTANCE_3D)
            projected_vertices.append(self.centre + projected_vertex*config.OBJECT_SCALE/self.polytope.bound)
            w_values.append(w_value)
        self.polytope.projected_vertices = np.array(projected_vertices)
        self.polytope.w_values = np.array(w_values)

    def render(self):
        self.display.screen.fill(config.BACKGROUND)
        rendering.draw_polytope(self.display, self.polytope)
        if self.display.w_values_enabled:
            rendering.draw_w_labels(self.display, self.polytope)
        if self.display.helper_legend_enabled:
            rendering.draw_helper_legend(self.display)
        rendering.draw_colour_legend(self.display, self.polytope)
        rendering.draw_rotation_angles_and_chosen_plane_text(self.display, self.angles, self.chosen_plane)
        pygame.display.update()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.display.clock.tick(config.FPS)
        pygame.quit()
