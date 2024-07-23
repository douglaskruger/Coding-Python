import json
import time
from bms import BatteryManagementSystem

def main():
    with open('config.json') as config_file:
        config = json.load(config_file)

    bms = BatteryManagementSystem(config['state_of_charge'], config['state_of_health'], config['voltage'], config['current'], config['temperature'], config['min_temperature'], config['max_temperature'])

    while True:
        print("\nBattery Management System")
        print("1. Charge")
        print("2. Discharge")
        print("3. Check Voltage")
        print("4. Check Current")
        print("5. Check Temperature")
        print("6. Display Status")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            bms.charge()
        elif choice == "2":
            bms.discharge()
        elif choice == "3":
            bms.check_voltage()
        elif choice == "4":
            bms.check_current()
        elif choice == "5":
            bms.check_temperature()
        elif choice == "6":
            bms.display_status()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

        bms.update_temperature()
        bms.calculate_state_of_health()
        bms.display_status()

        time.sleep(1)

if __name__ == "__main__":
    main()