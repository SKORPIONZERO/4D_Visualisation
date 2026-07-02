"""
rendering.py

"""
import config
import polytopes
import pygame

class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("4D Object Rotation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        self.w_values_enabled = True
        self.lerp_mode = 'hsv'  # Default to HSV mode

def draw_polytope(display: Display, polytope: polytopes.Polytope):
    display.screen.fill(config.BACKGROUND)
    for vertex in range(len(polytope.projected_vertices)):
        pygame.draw.circle(display.screen, config.BLUE, (int(polytope.projected_vertices[vertex][0]), int(polytope.projected_vertices[vertex][1])), 5)
    for edge in range(len(polytope.edges)):
        start_pos = polytope.projected_vertices[polytope.edges[edge][0]]
        for i in range(config.NUMBER_OF_LINE_SEGMENTS + 1):
            t = i / config.NUMBER_OF_LINE_SEGMENTS
            coordinates_t = polytope.projected_vertices[polytope.edges[edge][0]] + t * (polytope.projected_vertices[polytope.edges[edge][1]] - polytope.projected_vertices[polytope.edges[edge][0]])
            if display.lerp_mode == 'hsv':
                colours_t = config.lerp_colours_hsv(polytope.w_values[polytope.edges[edge][0]] + t * (polytope.w_values[polytope.edges[edge][1]] - polytope.w_values[polytope.edges[edge][0]]), polytope.bound)
            elif display.lerp_mode == 'rgb':
                colours_t = config.lerp_colours_rgb(polytope.w_values[polytope.edges[edge][0]] + t * (polytope.w_values[polytope.edges[edge][1]] - polytope.w_values[polytope.edges[edge][0]]), polytope.bound)
            else:
                raise ValueError("Invalid lerp_mode. Please choose 'rgb' or 'hsv'.")
            pygame.draw.line(display.screen, colours_t, start_pos, coordinates_t, 3)
            start_pos = coordinates_t
        pygame.draw.line(display.screen, config.WHITE, polytope.projected_vertices[polytope.edges[edge][0]], polytope.projected_vertices[polytope.edges[edge][1]], 2)

def draw_w_labels(display: Display, polytope: polytopes.Polytope):
    for i, vertex in enumerate(polytope.projected_vertices):
        text = display.font.render(f"{polytope.w_values[i]:.2f}", True, (255, 255, 255))
        display.screen.blit(text, (int(vertex[0]), int(vertex[1])))