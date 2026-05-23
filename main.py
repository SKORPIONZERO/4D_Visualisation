import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Window Dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive 4D Tesseract Viewer")
clock = pygame.time.Clock()

# Colors (RGB)
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
BLUE  = (0, 128, 255)

# --- 1. GEOMETRY SETUP ---
# A Tesseract has 16 vertices. We define them with 4 coordinates (X, Y, Z, W).
# We use -1 and 1 to center the shape at the origin (0,0,0,0).
vertices = []
for x in [-1, 1]:
    for y in [-1, 1]:
        for z in [-1, 1]:
            for w in [-1, 1]:
                vertices.append([x, y, z, w])

# Generate the 32 edges connecting the vertices of a tesseract
edges = []
for i in range(16):
    for j in range(i + 1, 16):
        # If two vertices differ by exactly one coordinate, they share an edge
        differences = 0
        for k in range(4):
            if vertices[i][k] != vertices[j][k]:
                differences += 1
        if differences == 1:
            edges.append((i, j))

# --- 2. ROTATION MATH ---
# To rotate in 4D, we must pick a plane to rotate within.
def rotate_xw(vertex, cos_a, sin_a):
    """Rotates the vertex in the X-W plane."""
    x, y, z, w = vertex
    return [x * cos_a - w * sin_a, y, z, x * sin_a + w * cos_a]

def rotate_yw(vertex, cos_a, sin_a):
    """Rotates the vertex in the Y-W plane."""
    x, y, z, w = vertex
    return [x, y * cos_a - w * sin_a, z, y * sin_a + w * cos_a]

# Current rotation tracking
angle_xw = 0
angle_yw = 0

# Control Settings
auto_rotate = True
rotation_speed = 1.0  # Degrees per frame

# Main Game Loop
running = True
while running:
    screen.fill(BLACK)
    
    # --- 3. HANDLE INPUTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Spacebar toggles automatic rotation
                auto_rotate = not auto_rotate

    # Manual controls (Hold keys to rotate manually)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle_xw -= rotation_speed
    if keys[pygame.K_RIGHT]:
        angle_xw += rotation_speed
    if keys[pygame.K_UP]:
        angle_yw -= rotation_speed
    if keys[pygame.K_DOWN]:
        angle_yw += rotation_speed

    # If auto-rotate is on, constantly increment the angles
    if auto_rotate:
        angle_xw += 0.5
        angle_yw += 0.5

    # Pre-calculate trig values for performance
    rad_xw = math.radians(angle_xw)
    cos_xw, sin_xw = math.cos(rad_xw), math.sin(rad_xw)
    rad_yw = math.radians(angle_yw)
    cos_yw, sin_yw = math.cos(rad_yw), math.sin(rad_yw)

    projected_2d_points = []

    for vertex in vertices:
        # Step A: Apply 4D Rotations
        rotated = rotate_xw(vertex, cos_xw, sin_xw)
        rotated = rotate_yw(rotated, cos_yw, sin_yw)
        
        x, y, z, w = rotated

        # Step B: 4D to 3D Perspective Projection
        # Distance of the 4D "camera" from the W axis
        distance_4d = 2.0 
        # Avoid division by zero if an object approaches the camera closely
        factor_4d = 1.0 / (distance_4d - w) if (distance_4d - w) != 0 else 1.0
        
        x3d = x * factor_4d
        y3d = y * factor_4d
        z3d = z * factor_4d

        # Step C: 3D to 2D Perspective Projection
        distance_3d = 2.0
        factor_3d = 1.0 / (distance_3d - z3d) if (distance_3d - z3d) != 0 else 1.0
        
        x2d = x3d * factor_3d
        y2d = y3d * factor_3d

        # Step D: Scale and center the points on the screen
        scale = 200
        screen_x = int(WIDTH / 2 + x2d * scale)
        screen_y = int(HEIGHT / 2 + y2d * scale)
        
        projected_2d_points.append((screen_x, screen_y))

    # --- 5. DRAWING THE EDGES ---
    for edge in edges:
        p1 = projected_2d_points[edge[0]]
        p2 = projected_2d_points[edge[1]]
        pygame.draw.line(screen, BLUE, p1, p2, 2)

    # Display simple instruction text
    font = pygame.font.SysFont(None, 24)
    text1 = font.render("SPACE: Toggle Auto-Rotate", True, WHITE)
    text2 = font.render("ARROW KEYS: Manual Rotate", True, WHITE)
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 35))

    pygame.display.flip()
    clock.tick(60) # Limit to 60 FPS

pygame.quit()
sys.exit()