import pygame
import math
import numpy as np

WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BACKGROUND = (30, 30, 30)
NEON_BLUE = (0, 150, 255)
ORANGE = (255, 100, 0)
GREEN = (0, 255, 0)

def setup():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("4D Tesseract Rotation Test - Orthographic Projection")
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
    Rxy, Rxz, Rxw, Ryz, Ryw, Rzw = define_rotation_matrices(theta)
    for k in range(len(line_vectors)):
        # Apply all rotation matrices in sequence
        rotated_vertex = Rxy @ Rxz @ Rxw @ Ryz @ Ryw @ Rzw @ line_vectors[k]
        current_vertex = centre + rotated_vertex * (cube_width // 2)
        current_vertices.append(current_vertex)
    return current_vertices

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

def main():
    screen, clock = setup()
    running = True
    centre = [screen.get_width() / 2, screen.get_height() / 2, 0, 0]
    cube_width = 200
    theta = 0
    theta_changing = False
    line_vectors=[]
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                for w in [-1, 1]:
                    line_vectors.append([x, y, z, w])
    while running:
        screen.fill(BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    theta_changing = not theta_changing
        current_vertices = calculate_vertices(centre, cube_width, line_vectors, theta)
        edges = calulate_edges(line_vectors)
        for vertex in current_vertices:
            pygame.draw.circle(screen, NEON_BLUE, (int(vertex[0]), int(vertex[1])), 5)
        for edge in edges:
            pygame.draw.line(screen, WHITE, current_vertices[edge[0]][:2], current_vertices[edge[1]][:2], 3)
        clock.tick(60)
        if theta_changing:
            theta = (theta + 0.01) % (2 * math.pi)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
