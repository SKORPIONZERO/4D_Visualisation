"""
rendering.py

Logic for rendering the polytope, its edges, and the w-values on the pygame window.
Contains the Display class, which manages the pygame window and its properties.
Displays the legend for controls, the colour legend, and the rotation planes text.
"""
import pygame

import config
import polytopes
import colouring

class Display:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("4D Object Rotation")
        self.clock = pygame.time.Clock()
        self.controls_font = pygame.font.SysFont("Courier New", 14)
        self.font = pygame.font.SysFont("Courier New", 18)

        self.w_values_enabled = True
        self.able_to_change_w_values_visibility = True  # Controls whether w-values can be turned on/off
        self.helper_legend_enabled = True
        self.fps_display_enabled = True  # Controls whether FPS display is shown
        self.lerp_mode = config.LERP_MODES['hsv']  # Default to HSV mode
        
        self.helper_legend_surface = self._build_helper_legend_surface()

    def _build_helper_legend_surface(self) -> pygame.Surface:
        """Pre-render text for legend for optimisation"""
        legend_texts = [
            "Controls:",
            "Q: Switch to Pentachoron(5-Cell)",
            "W: Switch to Tesseract(8-Cell)",
            "E: Switch to Hexadecachoron(16-Cell)",
            "A: Switch to Icositetrachoron(24-Cell)",
            "S: Switch to Hecatonicosachoron(120-Cell)",
            "D: Switch to Hexacontachoron(600-Cell)",
            "Turns off W-Values Display for better performance",
            "R: Reset the order and angles of rotation planes",
            "T: Turn W-Values Display On/Off",
            "H: Turn Helper Legend On/Off",
            "F: Turn FPS Display On/Off",
            "1-6: Select Rotation Plane",
            "(1) XY, (2) XZ, (3) XW, (4) YZ, (5) YW, (6) ZW",
            "->: Rotate Clockwise in chosen Plane",
            "<-: Rotate Anti-Clockwise in chosen Plane",
            "Z: Move the chosen plane to the left of the order",
            "X: Move the chosen plane to the right of the order",
            "Space: Turn Auto-Rotation On/Off",
            "Tab: Change Colour Interpolation Mode"
        ]
        line_height = 20
        rendered_lines = [self.controls_font.render(text, True, config.WHITE) for text in legend_texts]
        width = max(line.get_width() for line in rendered_lines)
        height = len(rendered_lines) * line_height
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        for i, line in enumerate(rendered_lines):
            surface.blit(line, (0, i * line_height))
        return surface

def draw_polytope(display: Display, polytope: polytopes.Polytope) -> None:
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

def draw_w_labels(display: Display, polytope: polytopes.Polytope) -> None:
    for i, vertex in enumerate(polytope.projected_vertices):
        text = display.font.render(f"{polytope.w_values[i]:.2f}", True, config.WHITE)
        display.screen.blit(text, (int(vertex[0]), int(vertex[1])))

def draw_helper_legend(display: Display) -> None:
    display.screen.blit(display.helper_legend_surface, (10, 10))

def draw_colour_legend(display: Display, polytope: polytopes.Polytope) -> None:
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
            raise ValueError("Invalid mode. Please choose 'rgb' or 'hsv'.")
        pygame.draw.line(display.screen, colour, (legend_x + i, legend_y), (legend_x + i, legend_y + legend_height), 1)
    # Draw the min and max w values
    min_text = display.font.render(f"{-polytope.bound:.2f}", True, config.WHITE)
    max_text = display.font.render(f"{polytope.bound:.2f}", True, config.WHITE)
    name_text = display.font.render("W Value", True, config.WHITE)
    display.screen.blit(name_text, (legend_x + (legend_width - name_text.get_width()) / 2, legend_y - 25))
    display.screen.blit(min_text, (legend_x - min_text.get_width() / 2, legend_y + 20))
    display.screen.blit(max_text, (legend_x + legend_width - max_text.get_width() / 2 - 5, legend_y + 20))

def draw_rotation_planes_text(display: Display, angles: dict, chosen_plane: str, order_rotation_applied: tuple) -> None:
    for i, (plane, angle) in enumerate(reversed(angles.items())):
        text = display.font.render(f"{plane}: {angle:.2f} rad", True, config.WHITE)
        display.screen.blit(text, (10, display.screen.get_height() - 50 - i * 30))
    # Draw the chosen plane and the order of rotation applied
    chosen_plane_text = display.font.render(f"Chosen Plane: {chosen_plane}", True, config.WHITE)
    order_text = display.font.render(f"Order of Rotation Applied: {' -> '.join(list(order_rotation_applied))}", True, config.WHITE)
    display.screen.blit(chosen_plane_text, (display.screen.get_width() - chosen_plane_text.get_width() - 10, display.screen.get_height() - 50))
    display.screen.blit(order_text, (display.screen.get_width() - order_text.get_width() - 10, display.screen.get_height() - 80))

def draw_fps(display: Display) -> None:
    fps_text = display.font.render(f"FPS: {int(display.clock.get_fps())}", True, config.WHITE)
    display.screen.blit(fps_text, (10, display.screen.get_height() - 230))






# rendering.py — add a helper for drawing a loading frame
def draw_loading_screen(display: Display, message: str) -> None:
    display.screen.fill(config.BACKGROUND)
    text = display.font.render(message, True, config.WHITE)
    text_rect = text.get_rect(center=(display.screen.get_width() / 2, display.screen.get_height() / 2))
    display.screen.blit(text, text_rect)
    pygame.display.update()