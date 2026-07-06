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
        # self.polytopes_by_key = {
        #     pygame.K_q: polytopes.Pentachoron_5_Cell(),
        #     pygame.K_w: polytopes.Tesseract_8_Cell(),
        #     pygame.K_e: polytopes.Hexadecachoron_16_Cell(),
        #     pygame.K_a: polytopes.Icositetrachoron_24_Cell(),
        #     pygame.K_s: polytopes.Hecatonicosachoron_120_Cell()
        # }
        # self.polytope = self.polytopes_by_key[pygame.K_w]  # Default polytope is Tesseract_8_Cell

        polytope_builders = [
            ("Pentachoron (5-Cell)", pygame.K_q, polytopes.Pentachoron_5_Cell),
            ("Tesseract (8-Cell)", pygame.K_w, polytopes.Tesseract_8_Cell),
            ("Hexadecachoron (16-Cell)", pygame.K_e, polytopes.Hexadecachoron_16_Cell),
            ("Icositetrachoron (24-Cell)", pygame.K_a, polytopes.Icositetrachoron_24_Cell),
            ("Hecatonicosachoron (120-Cell)", pygame.K_s, polytopes.Hecatonicosachoron_120_Cell),
            ("Hexacontachoron (600-Cell)", pygame.K_d, polytopes.Hexacosichoron_600_Cell)
        ]

        self.polytopes_by_key = {}
        for i, (name, key, builder) in enumerate(polytope_builders):
            rendering.draw_loading_screen(self.display, f"Loading {name}... ({i + 1}/{len(polytope_builders)})")
            self.polytopes_by_key[key] = builder()

        self.polytope = self.polytopes_by_key[pygame.K_w]  # default to Tesseract

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
                if event.key in self.polytopes_by_key:
                    self.polytope = self.polytopes_by_key[event.key]
                    if event.key == pygame.K_s or event.key == pygame.K_d:
                        # Turns off w-values display for better performance
                        self.display.able_to_change_w_values_visibility = False  # Disable the ability to turn w-values on/off for this polytope
                        self.display.w_values_enabled = False
                    else:
                        self.display.able_to_change_w_values_visibility = True
                        self.display.w_values_enabled = True
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
                elif event.key == pygame.K_f:
                    self.display.fps_display_enabled = not self.display.fps_display_enabled
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
        composed_rotation_matrix = rotation.compose_rotation_matrices(self.angles, self.order_rotation_applied)
        rotated_vertices = (composed_rotation_matrix @ self.polytope.vertices.T).T
        projected_vertices, w_values = projection.project_multiple_4D_to_2D(rotated_vertices, config.DISTANCE_4D, config.DISTANCE_3D)
        self.polytope.projected_vertices = self.centre + projected_vertices*config.OBJECT_SCALE/self.polytope.bound
        self.polytope.w_values = w_values

    def render(self) -> None:
        rendering.draw_polytope(self.display, self.polytope)
        if self.display.w_values_enabled:
            rendering.draw_w_labels(self.display, self.polytope)
        if self.display.helper_legend_enabled:
            rendering.draw_helper_legend(self.display)
        rendering.draw_colour_legend(self.display, self.polytope)
        rendering.draw_rotation_planes_text(self.display, self.angles, self.chosen_plane, self.order_rotation_applied)
        if self.display.fps_display_enabled:
            rendering.draw_fps(self.display)
        pygame.display.update()
    
    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.display.clock.tick(config.FPS)
        pygame.quit()
