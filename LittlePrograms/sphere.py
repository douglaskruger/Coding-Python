import turtle
import math

# Create a new turtle screen and set its background color
screen = turtle.Screen()
screen.bgcolor("white")

# Create a new turtle object
my_turtle = turtle.Turtle()

# Set the speed of the turtle
my_turtle.speed(0)

# Set the radius of the sphere
radius = 50

# Set the number of meridians (lines of longitude)
meridians = 20

# Set the number of parallels (lines of latitude)
parallels = 10

# Draw the sphere
for i in range(meridians):
    my_turtle.penup()
    my_turtle.goto(radius * math.cos(2 * math.pi * i / meridians), radius * math.sin(2 * math.pi * i / meridians))
    my_turtle.pendown()
    for j in range(parallels):
        my_turtle.goto(radius * math.cos(2 * math.pi * i / meridians) * math.cos(math.pi * j / parallels), radius * math.sin(2 * math.pi * i / meridians) * math.cos(math.pi * j / parallels))

# Draw the longitude lines
my_turtle.penup()
my_turtle.goto(0, 0)
my_turtle.pendown()
for i in range(meridians):
    my_turtle.goto(radius * math.cos(2 * math.pi * i / meridians), radius * math.sin(2 * math.pi * i / meridians))
    my_turtle.goto(-radius * math.cos(2 * math.pi * i / meridians), -radius * math.sin(2 * math.pi * i / meridians))

# Draw the latitude lines
my_turtle.penup()
my_turtle.goto(0, 0)
my_turtle.pendown()
for j in range(parallels):
    my_turtle.goto(radius * math.cos(math.pi * j / parallels), radius * math.sin(math.pi * j / parallels))
    my_turtle.goto(-radius * math.cos(math.pi * j / parallels), -radius * math.sin(math.pi * j / parallels))

# Keep the window open
turtle.done()