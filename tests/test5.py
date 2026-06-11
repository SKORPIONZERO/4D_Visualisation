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
    pygame.display.set_caption("3D Cube Rotation Test (single axis at a time) - Perspective Projection")
    clock = pygame.time.Clock()
    return screen, clock

def define_rotation_matrices(theta):
    """Defines rotation matrices for X, Y, and Z axes."""
    Rx = np.array([
        [1, 0, 0],
        [0, math.cos(theta), -math.sin(theta)],
        [0, math.sin(theta), math.cos(theta)]
    ])
    Ry = np.array([
        [math.cos(theta), 0, math.sin(theta)],
        [0, 1, 0],
        [-math.sin(theta), 0, math.cos(theta)]
    ])
    Rz = np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
    ])
    return Rx, Ry, Rz

def calculate_vertices(centre, cube_width, line_vectors, theta):
    """Calculates the current vertices for each rotation axis."""
    current_vertices1 = []
    current_vertices2 = []
    current_vertices3 = []
    Rx, Ry, Rz = define_rotation_matrices(theta)
    distance = 4
    for k in range(len(line_vectors)):
        # Cube 1
        rotated_vertex_1 = Rx @ line_vectors[k]
        factor = distance / (distance - rotated_vertex_1[2])
        current_vertex_1 = centre + [-350, 0, 0] + rotated_vertex_1 * (cube_width//2) * factor
        current_vertices1.append(current_vertex_1)
        # Cube 2
        rotated_vertex_2 = Ry @ line_vectors[k]
        factor = distance / (distance - rotated_vertex_2[2])
        current_vertex_2 = centre + [0, 0, 0] + rotated_vertex_2 * (cube_width//2) * factor
        current_vertices2.append(current_vertex_2)
        # Cube 3
        rotated_vertex_3 = Rz @ line_vectors[k]
        factor = distance / (distance - rotated_vertex_3[2])
        current_vertex_3 = centre + [350, 0, 0] + rotated_vertex_3 * (cube_width//2) * factor
        current_vertices3.append(current_vertex_3)
    return np.array(current_vertices1), np.array(current_vertices2), np.array(current_vertices3)

def calulate_edges(line_vectors):
    '''Defines edges based on the original line_vectors (not the rotated ones),
    since the connectivity doesn't change with rotation.'''
    # Two vertices share an edge if they differ by exactly one coordinate.
    edges = []
    for i in range(len(line_vectors)):
        for j in range(i + 1, len(line_vectors)):
            differences = 0
            for m in range(3):
                if line_vectors[i][m] != line_vectors[j][m]:
                    differences += 1
            if differences == 1:
                edges.append((i, j))
    return np.array(edges)

def main():
    screen, clock = setup()
    running = True
    centre=pygame.Vector3([screen.get_width() / 2, screen.get_height() / 2, 0])
    cube_width = 200
    edges = 12
    theta=0
    line_vectors=[]
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                line_vectors.append([x, y, z])
    theta_changing = False
    while running:
        screen.fill(BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    theta_changing = not theta_changing

        current_vertices1, current_vertices2, current_vertices3 = calculate_vertices(
            centre, cube_width, line_vectors, theta
            )
        edges = calulate_edges(line_vectors)
        
        # Drawing the vertices and the edges for each rotation axis using only the x and y coordinates for display
        for i in current_vertices1:
            pygame.draw.circle(screen, ORANGE, [int(i[0]), int(i[1])], 5)
        for i in current_vertices2:
            pygame.draw.circle(screen, BLUE, [int(i[0]), int(i[1])], 5)
        for i in current_vertices3:
            pygame.draw.circle(screen, GREEN, [int(i[0]), int(i[1])], 5)
        for j in edges:
            pygame.draw.line(screen, NEON_BLUE, current_vertices1[j[0]][:2], current_vertices1[j[1]][:2], 3)
            pygame.draw.line(screen, ORANGE, current_vertices2[j[0]][:2], current_vertices2[j[1]][:2], 3)
            pygame.draw.line(screen, WHITE, current_vertices3[j[0]][:2], current_vertices3[j[1]][:2], 3)
        clock.tick(60)
        if theta_changing:
            theta = (theta + 0.01) % (2 * math.pi)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
