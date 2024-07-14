import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants
G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
AU = 1.496e11  # Astronomical unit in meters
DAY = 60 * 60 * 24  # Day in seconds
YEAR = 365.25 * DAY  # Year in seconds

# Masses of the sun and planets
SUN_MASS = 1.989e30  # Mass of the sun in kg
MERCURY_MASS = 3.301e23  # Mass of Mercury in kg
VENUS_MASS = 4.867e24  # Mass of Venus in kg
EARTH_MASS = 5.972e24  # Mass of Earth in kg
MARS_MASS = 6.417e23  # Mass of Mars in kg
JUPITER_MASS = 1.898e27  # Mass of Jupiter in kg
SATURN_MASS = 5.683e26  # Mass of Saturn in kg
URANUS_MASS = 8.681e25  # Mass of Uranus in kg
NEPTUNE_MASS = 1.024e26  # Mass of Neptune in kg

# Initial positions of the planets (average distance from the sun)
MERCURY_DIST = 57.9e9  # Average distance of Mercury from the sun in meters
VENUS_DIST = 108.2e9  # Average distance of Venus from the sun in meters
EARTH_DIST = 149.6e9  # Average distance of Earth from the sun in meters
MARS_DIST = 227.9e9  # Average distance of Mars from the sun in meters
JUPITER_DIST = 778.3e9  # Average distance of Jupiter from the sun in meters
SATURN_DIST = 1.427e12  # Average distance of Saturn from the sun in meters
URANUS_DIST = 2.871e12  # Average distance of Uranus from the sun in meters
NEPTUNE_DIST = 4.497e12  # Average distance of Neptune from the sun in meters

# Initial velocities of the planets
MERCURY_VEL = 47.4e3  # Velocity of Mercury in m/s
VENUS_VEL = 35.0e3  # Velocity of Venus in m/s
EARTH_VEL = 29.8e3  # Velocity of Earth in m/s
MARS_VEL = 24.1e3  # Velocity of Mars in m/s
JUPITER_VEL = 13.1e3  # Velocity of Jupiter in m/s
SATURN_VEL = 9.7e3  # Velocity of Saturn in m/s
URANUS_VEL = 6.8e3  # Velocity of Uranus in m/s
NEPTUNE_VEL = 5.4e3  # Velocity of Neptune in m/s

class Planet:
    def __init__(self, mass, x, y, vx, vy):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.trace_x = [x]
        self.trace_y = [y]

    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.trace_x.append(self.x)
        self.trace_y.append(self.y)

    def update_velocity(self, dt, ax, ay):
        self.vx += ax * dt
        self.vy += ay * dt

def calculate_acceleration(planet1, planet2):
    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y
    r = np.sqrt(dx**2 + dy**2)
    a = G * planet2.mass / r**2
    ax = a * dx / r
    ay = a * dy / r
    return ax, ay

def update_planets(planets, dt):
    for i in range(len(planets)):
        for j in range(len(planets)):
            if i != j:
                ax, ay = calculate_acceleration(planets[i], planets[j])
                planets[i].update_velocity(dt, ax, ay)
        planets[i].update_position(dt)

def animate(i):
    update_planets(planets, DAY)
    positions = [[planet.x / AU, planet.y / AU] for planet in planets]
    scatter.set_offsets(positions)
    for planet, line in zip(planets, lines):
        line.set_data(np.array(planet.trace_x) / AU, np.array(planet.trace_y) / AU)
    return scatter,

# Create the planets
sun = Planet(SUN_MASS, 0, 0, 0, 0)
mercury = Planet(MERCURY_MASS, MERCURY_DIST, 0, 0, MERCURY_VEL)
venus = Planet(VENUS_MASS, VENUS_DIST, 0, 0, VENUS_VEL)
earth = Planet(EARTH_MASS, EARTH_DIST, 0, 0, EARTH_VEL)
mars = Planet(MARS_MASS, MARS_DIST, 0, 0, MARS_VEL)
jupiter = Planet(JUPITER_MASS, JUPITER_DIST, 0, 0, JUPITER_VEL)
saturn = Planet(SATURN_MASS, SATURN_DIST, 0, 0, SATURN_VEL)
uranus = Planet(URANUS_MASS, URANUS_DIST, 0, 0, URANUS_VEL)
neptune = Planet(NEPTUNE_MASS, NEPTUNE_DIST, 0, 0, NEPTUNE_VEL)

planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

fig = plt.figure()
ax = plt.axes(xlim=(-40, 40), ylim=(-40, 40))
scatter = ax.scatter([planet.x / AU for planet in planets], [planet.y / AU for planet in planets], s=[20*planet.mass/SUN_MASS for planet in planets])
lines = [ax.plot([], [], lw=0.5)[0] for _ in planets]

ani = animation.FuncAnimation(fig, animate, frames=365, interval=10, blit=True)

plt.show()
