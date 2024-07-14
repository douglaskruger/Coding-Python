import pygame
import math

# Constants
WIDTH, HEIGHT = 640, 480
CUBE_SIZE = 200

# Colors
WHITE = (255, 255, 255)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Variables
angle_x, angle_y = 0, 0
dragging = False
previous_mouse_position = None

# Function to project 3D points to 2D screen
def project(x, y, z):
    x -= WIDTH / 2
    y -= HEIGHT / 2
    z -= CUBE_SIZE / 2

    x = x * math.cos(angle_y) - z * math.sin(angle_y)
    z = x * math.sin(angle_y) + z * math.cos(angle_y)

    y = y * math.cos(angle_x) - z * math.sin(angle_x)
    z = y * math.sin(angle_x) + z * math.cos(angle_x)

    x += WIDTH / 2
    y += HEIGHT / 2

    return x, y

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            if previous_mouse_position is not None:
                dx, dy = event.pos[0] - previous_mouse_position[0], event.pos[1] - previous_mouse_position[1]
                angle_x += dy / 100
                angle_y += dx / 100
            previous_mouse_position = event.pos

    # Draw background
    screen.fill((0, 0, 0))

    # Draw cube
    points = [
        [-1, -1, -1],
        [1, -1, -1],
        [1, 1, -1],
        [-1, 1, -1],
        [-1, -1, 1],
        [1, -1, 1],
        [1, 1, 1],
        [-1, 1, 1],
    ]

    projected_points = [(project(x * CUBE_SIZE / 2, y * CUBE_SIZE / 2, z * CUBE_SIZE / 2)) for x, y, z in points]

    for i in range(4):
        p1 = projected_points[i]
        p2 = projected_points[(i + 1) % 4]
        p3 = projected_points[i + 4]
        p4 = projected_points[((i + 1) % 4) + 4]
        pygame.draw.line(screen, WHITE, p1, p2)
        pygame.draw.line(screen, WHITE, p1, p3)
        pygame.draw.line(screen, WHITE, p2, p4)
        pygame.draw.line(screen, WHITE, p3, p4)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
