import graphics
import math

def draw_polygon(num_points):
    # Create a new graphics window
    win = graphics.GraphWin("Polygon", 500, 500)

    # Calculate the angle between points
    angle = 360 / num_points

    # Initialize the starting point
    x, y = 250, 250

    # Draw the polygon
    for _ in range(num_points):
        # Calculate the next point
        next_x = x + 100 * math.cos(math.radians(angle * _))
        next_y = y + 100 * math.sin(math.radians(angle * _))

        # Draw a line from the current point to the next point
        line = graphics.Line(graphics.Point(x, y), graphics.Point(next_x, next_y))
        line.draw(win)

        # Update the current point
        x, y = next_x, next_y

    # Wait for a mouse click to close the window
    win.getMouse()
    win.close()

while True:
    # Ask the user for the number of points
    num_points = int(input("Enter the number of points for the polygon (or 0 to quit): "))

    if num_points == 0:
        break

    # Draw the polygon
    draw_polygon(num_points)