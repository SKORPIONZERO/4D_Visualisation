import pygame
import math
import numpy as np

WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (30, 30, 30)
NEON_BLUE = (0, 150, 255)
ORANGE = (255, 100, 0)

def setup():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Square rotation test")
    clock = pygame.time.Clock()
    return screen, clock

def main():
    screen, clock = setup()
    centre=pygame.Vector2([screen.get_width() / 2, screen.get_height() / 2])
    square_width = 200
    theta=0
    square = pygame.Rect(centre[0]-square_width//2,centre[1]-square_width//2,square_width,square_width)
    square_vertices = np.array([
        [square[0], square[1]],
        [square[0]+square[2], square[1]],
        [square[0]+square[2], square[1]+square[3]],
        [square[0], square[1]+square[3]]
    ])
    line_vectors = np.array([
        [-square_width//2,-square_width//2],
        [square_width//2,-square_width//2],
        [square_width//2,square_width//2],
        [-square_width//2,square_width//2]
    ])
    theta_changing = False
    running = True
    while running:
        screen.fill(BACKGROUND)
        R=np.array([
            [math.cos(theta), -math.sin(theta)], 
            [math.sin(theta), math.cos(theta)]
        ])
        current_vertices=[]
        for k in range(len(line_vectors)):
            current_vertices.append(centre +R @ line_vectors[k])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    theta_changing = not theta_changing
        pygame.draw.rect(surface=screen, color=WHITE, rect=square, width=2)
        for i in current_vertices:
            pygame.draw.circle(screen, ORANGE, i, 5)
        for j in range(len(current_vertices)):
            pygame.draw.line(screen, NEON_BLUE, current_vertices[j], current_vertices[(j+1)%len(current_vertices)], 3)
        clock.tick(120)
        if theta_changing:
            theta = (theta + 0.01) % (2 * math.pi)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
