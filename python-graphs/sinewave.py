#!/usr/bin/env python
# *******************************************************************
# Simple Sine Wave graph for Python
# *******************************************************************
import numpy as np
import matplotlib.pyplot as plot

# Get x values of the sine wave
time = np.arange(0, 10, 0.1);

# Amplitude of the sine wave is sine of a variable like time
amplitude = np.sin(time)

# Plot a sine wave using time and amplitude obtained for the sine wave
plot.plot(time, amplitude)

# Give a title for the sine wave plot
plot.title('Sine wave')

# Give x and y axis label for the sine wave plot
plot.xlabel('Time')
plot.ylabel('Amplitude = sin(time)')

# Draw grid and horizontal lines
plot.grid(True, which='both')
plot.axhline(y=0, color='k')

# Display the sine wave
plot.show()
