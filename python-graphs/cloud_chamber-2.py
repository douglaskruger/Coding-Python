import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import numpy as np

# Create a new figure
fig = plt.figure()
fig.canvas.set_window_title('Cloud Chamber')

# Set the dimensions of the figure
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))

# Initialize empty lists to store the x and y positions of the particles
alpha_x, alpha_y = [], []
beta_x, beta_y = [], []

# Initialize the plots for the alpha and beta particles
alpha_plot, = ax.plot([], [], 'ro', markersize=2)
beta_plot, = ax.plot([], [], 'bo', markersize=0.5)

# Function to initialize the animation
def init():
    alpha_plot.set_data([], [])
    beta_plot.set_data([], [])
    return alpha_plot, beta_plot,

# Function to animate the movement of the particles
def animate(i):
    # Randomly generate new positions for the alpha and beta particles
    new_alpha_x = np.random.uniform(0, 10)
    new_alpha_y = np.random.uniform(0, 10)
    new_beta_x = np.random.uniform(0, 10)
    new_beta_y = np.random.uniform(0, 10)

    # Append the new positions to the lists
    alpha_x.append(new_alpha_x)
    alpha_y.append(new_alpha_y)
    beta_x.append(new_beta_x)
    beta_y.append(new_beta_y)

    # Update the plots with the new data
    alpha_plot.set_data(alpha_x, alpha_y)
    beta_plot.set_data(beta_x, beta_y)

    return alpha_plot, beta_plot,

# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=100, interval=50, blit=True, init_func=init)

# Create a new axes for the clear button
clear_button_ax = plt.axes([0.7, 0.01, 0.1, 0.05])

# Create the clear button
clear_button = Button(clear_button_ax, 'Clear', color='lightgoldenrodyellow', hovercolor='0.975')

# Function to clear the screen
def clear(event):
    global alpha_x, alpha_y, beta_x, beta_y
    alpha_x, alpha_y = [], []
    beta_x, beta_y = [], []
    alpha_plot.set_data([], [])
    beta_plot.set_data([], [])

# Connect the function to the clear button
clear_button.on_clicked(clear)

# Create a new axes for the quit button
quit_button_ax = plt.axes([0.81, 0.01, 0.1, 0.05])

# Create the quit button
quit_button = Button(quit_button_ax, 'Quit', color='lightgoldenrodyellow', hovercolor='0.975')

# Function to quit the program
def quit(event):
    plt.close('all')
    exit()

# Connect the function to the quit button
quit_button.on_clicked(quit)

# Display the animation
plt.show()
