import pygame
import math
import numpy as np
import colorsys

WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (30, 30, 30)
NEON_BLUE = (0, 150, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

def setup():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("4D Tesseract Rotation Test - Perspective Projection")
    clock = pygame.time.Clock()
    return screen, clock

def define_rotation_matrices(theta):
    """Defines rotation matrices for all 6 coordinate planes in 4D (XY, XZ, XW, YZ, YW, ZW)."""
    c, s = math.cos(theta), math.sin(theta)
    Rxy = np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1]
    ])
    Rxz = np.array([
        [c, 0, -s, 0],
        [0, 1,  0, 0],
        [s, 0,  c, 0],
        [0, 0,  0, 1]
    ])
    Rxw = np.array([
        [c, 0, 0, -s],
        [0, 1, 0,  0],
        [0, 0, 1,  0],
        [s, 0, 0,  c]
    ])
    Ryz = np.array([
        [1, 0,  0, 0],
        [0, c, -s, 0],
        [0, s,  c, 0],
        [0, 0,  0, 1]
    ])
    Ryw = np.array([
        [1, 0, 0,  0],
        [0, c, 0, -s],
        [0, 0, 1,  0],
        [0, s, 0,  c]
    ])
    Rzw = np.array([
        [1, 0, 0,  0],
        [0, 1, 0,  0],
        [0, 0, c, -s],
        [0, 0, s,  c]
    ])
    return Rxy, Rxz, Rxw, Ryz, Ryw, Rzw

def calculate_vertices(centre, cube_width, line_vectors, theta):
    """Calculates the current vertices for each rotation axis."""
    current_vertices = []
    w_values = []
    Rxy, Rxz, Rxw, Ryz, Ryw, Rzw = define_rotation_matrices(theta)
    distance_4D = 3.0
    distance_3D = 4.0
    for k in range(len(line_vectors)):
        # Apply all rotation matrices in sequence
        rotated_vertex = Rxw @ Rxy @ Rxz @ Ryw @ Ryz @ Rzw @ line_vectors[k]
        x, y, z, w = rotated_vertex
        factor_4d = distance_4D/(distance_4D-w)
        x, y, z = x * factor_4d, y * factor_4d, z * factor_4d  # Apply 4D perspective projection
        factor_3d = distance_3D/(distance_3D-z)
        x, y = x * factor_3d, y * factor_3d  # Apply 3D perspective projection
        current_vertex = centre + np.array([x, y]) * (cube_width // 2)
        current_vertices.append(current_vertex)
        w_values.append(w)
    return current_vertices, w_values

def calulate_edges(line_vectors):
    '''Defines edges based on the original line_vectors (not the rotated ones),
    since the connectivity doesn't change with rotation.'''
    # Two vertices share an edge if they differ by exactly one coordinate.
    edges = []
    for i in range(len(line_vectors)):
        for j in range(i + 1, len(line_vectors)):
            differences = 0
            for m in range(4):
                if line_vectors[i][m] != line_vectors[j][m]:
                    differences += 1
            if differences == 1:
                edges.append((i, j))
    return np.array(edges)

def lerp_colours_rgb(value, max_value, min_value=None):
    R1, G1, B1 = BLUE
    R2, G2, B2 = RED
    if min_value is None:
        min_value = -max_value
    # Normalize v to a value between 0 and 1
    normalized_v = (value - min_value) / (max_value - min_value)
    # Map normalized_v to a color gradient between 2 colors, e.g., from blue to red.
    R_t = int(R1 + (R2 - R1) * normalized_v)
    G_t = int(G1 + (G2 - G1) * normalized_v)
    B_t = int(B1 + (B2 - B1) * normalized_v)
    return (R_t, G_t, B_t)

def lerp_colours_hsv(value, max_value, min_value=None):
    if min_value is None:
        min_value = -max_value
    saturation = 1.0
    value_brightness = 1.0
    # Normalize hue to a value between 0 and 1
    normalized_hue = (value - min_value) / (max_value - min_value)
    # Map normalized_hue to a color gradient in HSV space.
    hue = 240 * (1 - normalized_hue)  # From blue (240) to red (0)
    # Convert HSV to RGB
    r, g, b = colorsys.hsv_to_rgb(hue / 360.0, saturation, value_brightness)
    return (int(r * 255), int(g * 255), int(b * 255))

def lerp_colours(values,max_value, min_value=None, mode='rgb'):
    colours = []
    if mode == 'rgb':
        for v in values:
            colours.append(lerp_colours_rgb(v, max_value, min_value))
    elif mode == 'hsv':
        for v in values:
            colours.append(lerp_colours_hsv(v, max_value, min_value))
    return colours

def display_shape(screen, current_vertices, w_values, edges, colours, number_of_line_segments, max_distance_from_origin):
    for vertex in range(len(current_vertices)):
            pygame.draw.circle(screen, colours[vertex], (int(current_vertices[vertex][0]), int(current_vertices[vertex][1])), 10)
    for edge in range(len(edges)):
        start_pos = current_vertices[edges[edge][0]]
        for i in range(number_of_line_segments + 1):
            t = i / number_of_line_segments
            coordinates_t = current_vertices[edges[edge][0]] + t * (current_vertices[edges[edge][1]] - current_vertices[edges[edge][0]])
            colours_t = lerp_colours_hsv(w_values[edges[edge][0]] + t * (w_values[edges[edge][1]] - w_values[edges[edge][0]]), max_distance_from_origin)
            pygame.draw.line(screen, colours_t, start_pos, coordinates_t, 3)
        start_pos = coordinates_t    

def create_line_vectors(unit_distance):
    line_vectors=[]
    for x in [-unit_distance, unit_distance]:
        for y in [-unit_distance, unit_distance]:
            for z in [-unit_distance, unit_distance]:
                for w in [-unit_distance, unit_distance]:
                    line_vectors.append([x, y, z, w])
    return line_vectors

def main():
    screen, clock = setup()
    running = True
    centre = [screen.get_width() / 2, screen.get_height() / 2]
    cube_width = 200
    dimensions = 4
    unit_distance = 1
    number_of_line_segments = 20
    theta = 0
    theta_changing = False
    max_distance_from_origin = math.sqrt(dimensions) * unit_distance
    line_vectors = create_line_vectors(unit_distance)
    while running:
        screen.fill(BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    theta_changing = not theta_changing
        current_vertices, w_values = calculate_vertices(centre, cube_width, line_vectors, theta)
        edges = calulate_edges(line_vectors)
        colours = lerp_colours(w_values, max_distance_from_origin, mode='hsv')
        display_shape(screen, current_vertices, w_values, edges, colours, number_of_line_segments, max_distance_from_origin) 
        clock.tick(60)
        if theta_changing:
            theta = (theta + 0.01) % (2 * math.pi)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
