"""
rendering.py

"""
import config
import polytopes
import colouring
import pygame

class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("4D Object Rotation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        self.w_values_enabled = True
        self.lerp_mode = config.LERP_MODES['hsv']  # Default to HSV mode

def draw_polytope(display: Display, polytope: polytopes.Polytope):
    display.screen.fill(config.BACKGROUND)
    colours = colouring.lerp_colours(polytope.w_values, polytope.bound, mode=display.lerp_mode)
    for vertex in range(len(polytope.projected_vertices)):
        pygame.draw.circle(display.screen, colours[vertex], (int(polytope.projected_vertices[vertex][0]), int(polytope.projected_vertices[vertex][1])), 5)
    for edge in range(len(polytope.edges)):
        start_pos = polytope.projected_vertices[polytope.edges[edge][0]]
        for i in range(config.NUMBER_OF_LINE_SEGMENTS + 1):
            t = i / config.NUMBER_OF_LINE_SEGMENTS
            coordinates_t = polytope.projected_vertices[polytope.edges[edge][0]] + t * (polytope.projected_vertices[polytope.edges[edge][1]] - polytope.projected_vertices[polytope.edges[edge][0]])
            if display.lerp_mode == config.LERP_MODES['hsv']:
                colours_t = colouring.lerp_colours_hsv(polytope.w_values[polytope.edges[edge][0]] + t * (polytope.w_values[polytope.edges[edge][1]] - polytope.w_values[polytope.edges[edge][0]]), polytope.bound)
            elif display.lerp_mode == config.LERP_MODES['rgb']:
                colours_t = colouring.lerp_colours_rgb(polytope.w_values[polytope.edges[edge][0]] + t * (polytope.w_values[polytope.edges[edge][1]] - polytope.w_values[polytope.edges[edge][0]]), polytope.bound)
            else:
                raise ValueError("Invalid lerp_mode. Please choose 'rgb' or 'hsv'.")
            pygame.draw.line(display.screen, colours_t, start_pos, coordinates_t, 3)
            start_pos = coordinates_t

def draw_w_labels(display: Display, polytope: polytopes.Polytope):
    for i, vertex in enumerate(polytope.projected_vertices):
        text = display.font.render(f"{polytope.w_values[i]:.2f}", True, (255, 255, 255))
        display.screen.blit(text, (int(vertex[0]), int(vertex[1])))
        
def draw_colour_legend(display: Display, polytope: polytopes.Polytope):
    legend_height = 20
    legend_width = 200
    legend_x = display.screen.get_width() - legend_width - 20
    legend_y = 30

    for i in range(legend_width):
        t = i / (legend_width - 1)
        w_value = -polytope.bound + t * (2 * polytope.bound)
        if display.lerp_mode == config.LERP_MODES['hsv']:
            colour = colouring.lerp_colours_hsv(w_value, polytope.bound)
        elif display.lerp_mode == config.LERP_MODES['rgb']:
            colour = colouring.lerp_colours_rgb(w_value, polytope.bound)
        else:
            raise ValueError("Invalid lerp_mode. Please choose 'rgb' or 'hsv'.")
        pygame.draw.line(display.screen, colour, (legend_x + i, legend_y), (legend_x + i, legend_y + legend_height), 1)

    # Draw the min and max w values
    min_text = display.font.render(f"{-polytope.bound:.2f}", True, (255, 255, 255))
    max_text = display.font.render(f"{polytope.bound:.2f}", True, (255, 255, 255))
    name_text = display.font.render("W Value", True, (255, 255, 255))
    display.screen.blit(name_text, (legend_x + (legend_width - name_text.get_width()) / 2, legend_y - 30))
    display.screen.blit(min_text, (legend_x - min_text.get_width() + 18, legend_y + 20))
    display.screen.blit(max_text, (legend_x + legend_width - 22, legend_y + 20))