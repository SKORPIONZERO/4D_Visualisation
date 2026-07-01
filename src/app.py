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

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("4D Object Rotation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        
        self.running = True
        #self.w_values_enabled = True
        self.centre = np.array([self.screen.get_width() / 2, self.screen.get_height() / 2])     
        self.order_rotation_applied = config.PLANES
        #self.chosen_plane = config.PLANES[0]
        #self.angles = {plane: 0.0 for plane in config.PLANES}
        self.theta = 0.0
        #self.auto_rotation = {plane: False for plane in config.PLANES}
        self.auto_rotation = False
        #self.rotation_speeds = {plane: self.rotation_speed for plane in config.PLANES}

        self.polytope = polytopes.Tesseract()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #self.auto_rotation[self.chosen_plane] = not self.auto_rotation[self.chosen_plane]
                    self.auto_rotation = not self.auto_rotation
                if event.key == pygame.K_t:
                    #self.w_values_enabled = not self.w_values_enabled
                    pass
                for key, plane in config.PLANE_KEYS.items():
                    if event.key == key:
                        #self.chosen_plane = plane
                        pass
                # TODO: Add more event handling as needed (e.g., for rotation speed adjustment, changing objects)
    
    def update(self):
        if self.auto_rotation:
            self.theta = (self.theta + config.BASE_ROTATION_SPEED) % (2 * math.pi)
        # for plane in config.PLANES:
        #     if self.auto_rotation[plane]:
        #         self.angles[plane] = (self.angles[plane] + self.rotation_speed) % (2 * math.pi)
        #final_rotation_matrix = rotation.compose_rotation_matrices(self.angles, self.order_rotation_applied)
        #self.polytope.vertices = np.array([final_rotation_matrix @ vertex for vertex in self.polytope.vertices])
        Rxy, Rxz, Rxw, Ryz, Ryw, Rzw = rotation.define_rotation_matrices(self.theta)
        composed_rotation_matrix = Rxw @ Rxy @ Rxz @ Ryw @ Ryz @ Rzw
        projected_vertices, w_values = [], []
        for vertex in self.polytope.original_vertices:
            projected_vertex, w_value = projection.project_4D_to_2D(composed_rotation_matrix @ vertex, config.DISTANCE_4D, config.DISTANCE_3D)
            projected_vertices.append(self.centre + projected_vertex*config.OBJECT_SCALE)
            w_values.append(w_value)
        self.polytope.projected_vertices = np.array(projected_vertices)
        self.polytope.w_values = np.array(w_values)

    def render(self):
        self.screen.fill(config.BACKGROUND)
        for vertex in range(len(self.polytope.projected_vertices)):
            pygame.draw.circle(self.screen, config.BLUE, (int(self.polytope.projected_vertices[vertex][0]), int(self.polytope.projected_vertices[vertex][1])), 5)
        for edge in range(len(self.polytope.edges)):
            pygame.draw.line(self.screen, config.WHITE, self.polytope.projected_vertices[self.polytope.edges[edge][0]], self.polytope.projected_vertices[self.polytope.edges[edge][1]], 2)
        pygame.display.update()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(config.FPS)
        pygame.quit()
