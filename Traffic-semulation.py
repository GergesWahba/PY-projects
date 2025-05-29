"""
Author: Gerges
Date: 03/08/2022
Purpose: Traffic Light Control System Simulation (Python Version)
"""

def traffic_light_control(car_detected: bool, timer_condition: bool, pedestrian_crossing: bool) -> bool:
    """
    Determines if the traffic light should be green based on the given logic:
    (C ∨ T) ∧ ¬P
    """
    return (car_detected or timer_condition) and not pedestrian_crossing


def get_bool_input(prompt: str) -> bool:
    """Prompt user for 1 or 0 and return boolean value."""
    while True:
        try:
            value = int(input(prompt))
            if value in [0, 1]:
                return bool(value)
            else:
                print("Please enter 1 for Yes or 0 for No.")
        except ValueError:
            print("Invalid input. Please enter 1 or 0.")


def main():
    print("Traffic Light Control System Simulation")
    print("-------------------------------------------------------------")

    while True:
        car_detected = get_bool_input("Is a car detected? (1 for Yes, 0 for No): ")
        timer_condition = get_bool_input("Is the timer condition allowing? (1 for Yes, 0 for No): ")
        pedestrian_crossing = get_bool_input("Is a pedestrian crossing? (1 for Yes, 0 for No): ")

        green_light = traffic_light_control(car_detected, timer_condition, pedestrian_crossing)

        if green_light:
            print("Result: The traffic light is GREEN (Cars can go)")
        else:
            print("Result: The traffic light is RED (Cars must stop)")

        choice = input("Do you want to try again? (y/n): ").strip().lower()
        if choice != 'y':
            print("Simulation ended. Thank you!")
            print("-------------------------------------------------------------")
            break


if __name__ == "__main__":
    main()