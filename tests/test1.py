import pygame
import math
import numpy as np

WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

def setup():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Single line rotation test")
    clock = pygame.time.Clock()
    return screen, clock

def main():
    screen, clock = setup()
    running = True
    start = pygame.Vector2([screen.get_width() / 2, screen.get_height() / 2])
    line_vector1 = np.array([200, 0])
    line_vector2 = np.array([0, 250])
    theta = 0
    while running:
        screen.fill(BLACK)
        # Rotation matrix for the current total angle
        R = np.array(
            [[math.cos(theta), -math.sin(theta)], 
             [math.sin(theta), math.cos(theta)]
            ])
        
        # Calculate the actual end point: start position + rotated vector
        # current_end_x = start[0] + line_vector1[0]*R[0][0]+line_vector1[1]*R[0][1]
        # current_end_y = start[1] + line_vector1[0]*R[1][0]+line_vector1[1]*R[1][1]
        # current_end1=pygame.Vector2([current_end_x, current_end_y])

        # Flip the y-axis by subtracting from HEIGHT to make screen
        # coordinates match mathematical coordinates on a cartesian plane
        # current_end_y = HEIGHT-(start[1] + line_vector1[0]*R[1][0]+line_vector1[1]*R[1][1])
        
        # Previous 3 lines are equivalent to the next one
        current_end1 = start + R @ line_vector1
        
        current_end2 = start + R @ line_vector2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.draw.line(screen, BLUE, start, current_end1, 3)
        pygame.draw.line(screen, WHITE, start, current_end2, 3)
        theta = (theta + 0.05) % (2 * math.pi)
        clock.tick(60)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
