"""
app.py
 
App owns the pygame window, the clock, and the main loop. It holds
the states that change frame to frame (angles, whether auto rotation is
currently On/Off, whether w-coordinates values are shown) as instance attributes
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
    def __init__(self) -> None:
        self.display = rendering.Display()
        self.polytope = polytopes.Tesseract_8_Cell()
        
        self.running = True
        self.centre = np.array([self.display.screen.get_width() / 2, self.display.screen.get_height() / 2])
        self.auto_rotation = False
        self.order_rotation_applied = list(config.PLANES)
        self.chosen_plane = config.PLANES[0]
        self.angles = {plane: 0.0 for plane in config.PLANES}
    
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.polytope = polytopes.Pentachoron_5_Cell()
                elif event.key == pygame.K_w:
                    self.polytope = polytopes.Tesseract_8_Cell()
                elif event.key == pygame.K_e:
                    self.polytope = polytopes.Hexadecachoron_16_Cell()
                elif event.key == pygame.K_a:
                    self.polytope = polytopes.Icositetrachoron_24_Cell()
                elif event.key == pygame.K_s:
                    self.polytope = polytopes.Hecatonicosachoron_120_Cell()
                    self.display.able_to_change_w_values_visibility = False  # Disable the ability to turn w-values on/off for this polytope
                    self.display.w_values_enabled = False  # Turns off w-values display for better performance
                elif event.key == pygame.K_r:
                    self.order_rotation_applied = list(config.PLANES)
                    self.angles = {plane: 0.0 for plane in config.PLANES}
                    self.chosen_plane = config.PLANES[0]
                elif event.key == pygame.K_SPACE:
                    self.auto_rotation = not self.auto_rotation
                elif event.key == pygame.K_t and self.display.able_to_change_w_values_visibility:
                    self.display.w_values_enabled = not self.display.w_values_enabled
                elif event.key == pygame.K_h:
                    self.display.helper_legend_enabled = not self.display.helper_legend_enabled
                elif event.key == pygame.K_TAB:
                    self.display.lerp_mode = (self.display.lerp_mode + 1) % len(config.LERP_MODES)
                elif event.key == pygame.K_z:
                    # Move the chosen plane to the left of the order
                    index = self.order_rotation_applied.index(self.chosen_plane)
                    if index > 0:
                        self.order_rotation_applied[index], self.order_rotation_applied[index - 1] = self.order_rotation_applied[index - 1], self.order_rotation_applied[index]
                elif event.key == pygame.K_x:
                    # Move the chosen plane to the right of the order
                    index = self.order_rotation_applied.index(self.chosen_plane)
                    if index < len(self.order_rotation_applied) - 1:
                        self.order_rotation_applied[index], self.order_rotation_applied[index + 1] = self.order_rotation_applied[index + 1], self.order_rotation_applied[index]
                for key, plane in config.PLANE_KEYS.items():
                    if event.key == key:
                        self.chosen_plane = plane
        self.process_manual_key_rotation()

    def process_manual_key_rotation(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.angles[self.chosen_plane] = (self.angles[self.chosen_plane] + config.ROTATION_SPEED) % (2 * math.pi)
        elif keys[pygame.K_LEFT]:
            self.angles[self.chosen_plane] = (self.angles[self.chosen_plane] - config.ROTATION_SPEED) % (2 * math.pi)
    
    def update(self) -> None:
        if self.auto_rotation:
            for plane in config.PLANES:
                self.angles[plane] = (self.angles[plane] + config.ROTATION_SPEED) % (2 * math.pi)
        if type(self.polytope) is not polytopes.Hecatonicosachoron_120_Cell:
            self.display.able_to_change_w_values_visibility = True  # Re-enable the ability to turn w-values on/off for other polytopes
            self.w_values_enabled = True  # Ensure w-values are enabled for other polytopes
        composed_rotation_matrix = rotation.compose_rotation_matrices(self.angles, self.order_rotation_applied)
        projected_vertices, w_values = [], []
        for vertex in self.polytope.vertices:
            projected_vertex, w_value = projection.project_4D_to_2D(composed_rotation_matrix @ vertex, config.DISTANCE_4D, config.DISTANCE_3D)
            projected_vertices.append(self.centre + projected_vertex*config.OBJECT_SCALE/self.polytope.bound)
            w_values.append(w_value)
        self.polytope.projected_vertices = np.array(projected_vertices)
        self.polytope.w_values = np.array(w_values)

    def render(self) -> None:
        rendering.draw_polytope(self.display, self.polytope)
        if self.display.w_values_enabled:
            rendering.draw_w_labels(self.display, self.polytope)
        if self.display.helper_legend_enabled:
            rendering.draw_helper_legend(self.display)
        rendering.draw_colour_legend(self.display, self.polytope)
        rendering.draw_rotation_planes_text(self.display, self.angles, self.chosen_plane, self.order_rotation_applied)
        pygame.display.update()
    
    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.display.clock.tick(config.FPS)
        pygame.quit()
