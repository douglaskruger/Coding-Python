import math

def calculate_aerodynamic_forces(pitch_angle, blade_angle, blade_length, blade_width, air_density, air_temperature, revolutions_per_second, velocity, number_of_blades):
    # Calculate the angle of attack
    angle_of_attack = pitch_angle - blade_angle

    # Calculate the relative velocity
    relative_velocity = velocity + (2 * math.pi * revolutions_per_second * blade_length)

    # Calculate the lift and drag coefficients
    lift_coefficient = 2 * math.pi * angle_of_attack
    drag_coefficient = 2 * math.pi * (1 - math.cos(angle_of_attack))

    # Calculate the lift and drag forces
    lift_force = 0.5 * air_density * relative_velocity**2 * blade_width * lift_coefficient
    drag_force = 0.5 * air_density * relative_velocity**2 * blade_width * drag_coefficient

    # Calculate the thrust and torque
    thrust = number_of_blades * (lift_force * math.cos(blade_angle) - drag_force * math.sin(blade_angle))
    torque = number_of_blades * (lift_force * math.sin(blade_angle) + drag_force * math.cos(blade_angle)) * blade_length

    # Calculate the air viscosity
    air_viscosity = 1.458 * 10**(-6) * air_temperature**(3/2) / (air_temperature + 110.4)

    # Calculate the Reynolds number
    reynolds_number = air_density * relative_velocity * blade_length / air_viscosity

    # Calculate the drag coefficient correction
    drag_coefficient_correction = 1 - 0.035 * reynolds_number**(0.2)

    # Calculate the corrected drag force
    corrected_drag_force = drag_force * drag_coefficient_correction

    # Calculate the corrected thrust and torque
    corrected_thrust = number_of_blades * (lift_force * math.cos(blade_angle) - corrected_drag_force * math.sin(blade_angle))
    corrected_torque = number_of_blades * (lift_force * math.sin(blade_angle) + corrected_drag_force * math.cos(blade_angle)) * blade_length

    return corrected_thrust, corrected_torque, lift_force, corrected_drag_force

def get_user_input():
    pitch_angle = float(input("Enter the pitch angle in degrees (45): ") or 45)
    pitch_angle = math.radians(pitch_angle)

    blade_angle = float(input("Enter the blade angle in degrees (30): ") or 30)
    blade_angle = math.radians(blade_angle)

    blade_length = float(input("Enter the length of the blade in meters (1.5): ") or 1.5)
    blade_width = float(input("Enter the width of the blade in meters (0.2): ") or 0.2)

    air_density = float(input("Enter the air density in kg/m^3 (1.225): ") or 1.225)
    air_temperature = float(input("Enter the air temperature in Kelvin (293): ") or 293)
    revolutions_per_second = float(input("Enter the revolutions per second (10): ") or 10)
    velocity = float(input("Enter the velocity in m/s (50): ") or 50)

    number_of_blades = int(input("Enter the number of blades (4): ") or 4)

    return pitch_angle, blade_angle, blade_length, blade_width, air_density, air_temperature, revolutions_per_second, velocity, number_of_blades

def main():
    pitch_angle, blade_angle, blade_length, blade_width, air_density, air_temperature, revolutions_per_second, velocity, number_of_blades = get_user_input()

    thrust, torque, lift_force, drag_force = calculate_aerodynamic_forces(pitch_angle, blade_angle, blade_length, blade_width, air_density, air_temperature, revolutions_per_second, velocity, number_of_blades)

    print("Thrust: ", thrust, "N (", thrust * 0.224809, "lbs, ", thrust * 0.101972, "kg)")
    print("Torque: ", torque, "Nm (", torque * 0.737562, "lb feet)")
    print("Lift Force: ", lift_force, "N (", lift_force * 0.224809, "lbs, ", lift_force * 0.101972, "kg)")
    print("Drag Force: ", drag_force, "N (", drag_force * 0.224809, "lbs, ", drag_force * 0.101972, "kg)")

if __name__ == "__main__":
    main()