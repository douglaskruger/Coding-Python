class BatteryManagementSystem:
    def __init__(self, state_of_charge, state_of_health, voltage, current, temperature, min_temperature, max_temperature):
        self.state_of_charge = state_of_charge
        self.state_of_health = state_of_health
        self.voltage = voltage
        self.current = current
        self.temperature = temperature
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.room_temperature = 20
        self.depth_of_discharge = 0
        self.cycle_count = 0

    def charge(self):
        if self.temperature > self.max_temperature:
            print("Temperature is too high. Cannot charge.")
        elif self.temperature < self.min_temperature:
            print("Temperature is too low. Cannot charge.")
        elif self.state_of_charge < 80:
            self.state_of_charge += 10
            print("Charging...")
            self.temperature += 3
        else:
            print("Battery is fully charged.")

    def discharge(self):
        if self.temperature > self.max_temperature:
            print("Temperature is too high. Cannot discharge.")
        elif self.temperature < self.min_temperature:
            print("Temperature is too low. Cannot discharge.")
        elif self.state_of_charge > 20:
            self.state_of_charge -= 10
            print("Discharging...")
            self.temperature += 3
            self.depth_of_discharge += 10
            if self.depth_of_discharge >= 80:
                self.cycle_count += 1
                self.depth_of_discharge = 0
        else:
            print("Battery is fully discharged.")

    def check_voltage(self):
        if self.voltage > 4.2:
            print("Overvoltage! Voltage is", self.voltage)
        elif self.voltage < 3.2:
            print("Undervoltage! Voltage is", self.voltage)
        else:
            print("Voltage is normal.")

    def check_current(self):
        if self.current > 5:
            print("Overcurrent! Current is", self.current)
        else:
            print("Current is normal.")

    def check_temperature(self):
        if self.temperature > self.max_temperature:
            print("Overheating! Temperature is", self.temperature)
        elif self.temperature < self.min_temperature:
            print("Overcooling! Temperature is", self.temperature)
        else:
            print("Temperature is normal.")

    def display_status(self):
        print("State of Charge:", self.state_of_charge)
        print("State of Health:", self.state_of_health)
        print("Voltage:", self.voltage)
        print("Current:", self.current)
        print("Temperature:", self.temperature)

    def update_temperature(self):
        if self.temperature > self.room_temperature:
            self.temperature -= 3
            if self.temperature < self.room_temperature:
                self.temperature = self.room_temperature

    def calculate_state_of_health(self):
        self.state_of_health = 100 - (self.cycle_count * 2)
        if self.state_of_health < 0:
            self.state_of_health = 0