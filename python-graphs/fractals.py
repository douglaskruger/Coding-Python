import turtle

def tree(branch_len, t):
    if branch_len > 5:
        t.forward(branch_len)
        t.right(20)
        tree(branch_len-15, t)
        t.left(40)
        tree(branch_len-15, t)
        t.right(20)
        t.backward(branch_len)

def draw_tree():
    t = turtle.Turtle()
    my_win = turtle.Screen()
    t.left(90)
    t.up()
    t.backward(100)
    t.down()
    t.color("green")
    tree(75, t)
    my_win.exitonclick()

def draw_sierpinski(order, size):
    if order == 0:
        for _ in range(3):
            turtle.forward(size)
            turtle.right(120)
    else:
        draw_sierpinski(order-1, size/2)
        turtle.forward(size/2)
        draw_sierpinski(order-1, size/2)
        turtle.backward(size/2)
        turtle.left(60)
        turtle.forward(size/2)
        turtle.right(60)
        draw_sierpinski(order-1, size/2)
        turtle.left(60)
        turtle.backward(size/2)
        turtle.right(60)

def draw_sierpinski_triangle():
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-200, -150)
    turtle.pendown()
    draw_sierpinski(5, 400)
    turtle.done()

def draw_koch_curve(turtle, iterations, length):
    if iterations == 0:
        turtle.forward(length)
    else:
        iterations -= 1
        length /= 3
        draw_koch_curve(turtle, iterations, length)
        turtle.left(60)
        draw_koch_curve(turtle, iterations, length)
        turtle.right(120)
        draw_koch_curve(turtle, iterations, length)
        turtle.left(60)
        draw_koch_curve(turtle, iterations, length)

def draw_koch_snowflake():
    t = turtle.Turtle()
    my_win = turtle.Screen()
    t.speed(0)
    for _ in range(3):
        draw_koch_curve(t, 4, 400)
        t.right(120)
    my_win.exitonclick()

#draw_tree()
#draw_sierpinski_triangle()
draw_koch_snowflake()
