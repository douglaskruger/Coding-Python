import pygame
import math

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
size = (WIDTH, HEIGHT)
cx, cy = WIDTH // 2, HEIGHT // 2
fov = min(WIDTH, HEIGHT)

# Create the window
screen = pygame.display.set_mode(size)

# Set up the cube
cube_points = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
               (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]

# Set up the camera
camera_x, camera_y = 0, 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the mouse position and buttons
    mx, my = pygame.mouse.get_pos()
    buttons = pygame.mouse.get_pressed()

    # Rotate the cube if the left mouse button is clicked
    if buttons[0]:
        camera_x += (mx - cx) / fov
        camera_y += (my - cy) / fov

    # Set up the rotation matrix
    rotation_x = [[1, 0, 0],
                  [0, math.cos(camera_x), -math.sin(camera_x)],
                  [0, math.sin(camera_x), math.cos(camera_x)]]

    rotation_y = [[math.cos(camera_y), 0, math.sin(camera_y)],
                  [0, 1, 0],
                  [-math.sin(camera_y), 0, math.cos(camera_y)]]

    # Apply the rotation to the cube points
    points = []
    for point in cube_points:
        x = point[0] * rotation_x[0][0] + point[1] * rotation_x[0][1] + point[2] * rotation_x[0][2]
        y = point[0] * rotation_x[1][0] + point[1] * rotation_x[1][1] + point[2] * rotation_x[1][2]
        z = point[0] * rotation_x[2][0] + point[1] * rotation_x[2][1] + point[2] * rotation_x[2][2]

        x = x * rotation_y[0][0] + y * rotation_y[0][1] + z * rotation_y[0][2]
        y = x * rotation_y[1][0] + y * rotation_y[1][1] + z * rotation_y[1][2]
        z = x * rotation_y[2][0] + y * rotation_y[2][1] + z * rotation_y[2][2]

        x = x * fov / (4 + z) + cx
        y = y * fov / (4 + z) + cy

        points.append((x, y))

    # Draw everything
    screen.fill((0, 0, 0))
    for i in range(4):
        p1 = points[i]
        p2 = points[(i + 1) % 4]
        p3 = points[i + 4]
        p4 = points[((i + 1) % 4) + 4]
        pygame.draw.line(screen, (255, 255, 255), p1, p2)
        pygame.draw.line(screen, (255, 255, 255), p3, p4)
        pygame.draw.line(screen, (255, 255, 255), p1, p3)

    pygame.display.flip()
