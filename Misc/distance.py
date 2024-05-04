import matplotlib.pyplot as plt
import numpy as np

def calculate_distance(initial_velocity, time, acceleration):
    distance = (initial_velocity * time) + (0.5 * acceleration * (time ** 2))
    return distance


def plot_distance_vs_time(initial_velocity, time, acceleration):
    # Generate an array of time values from 0 to the given time
    time_array = np.linspace(0, time, 100)

    # Calculate the distance for each time value
    distance_array = [calculate_distance(initial_velocity, t, acceleration) for t in time_array]

    # Create the plot
    plt.plot(time_array, distance_array)
    plt.xlabel('Time (s)')
    plt.ylabel('Distance (m)')
    plt.title('Distance vs Time')
    plt.grid(True)
    plt.show()


# Usage
initial_velocity = float(input("Enter the initial velocity (in meters per second): "))
time = float(input("Enter the time (in seconds): "))
acceleration = float(input("Enter the acceleration (in meters per second squared): "))

distance = calculate_distance(initial_velocity, time, acceleration)

print("The distance traveled is: ", distance, "meters")

plot_distance_vs_time(initial_velocity, time, acceleration)