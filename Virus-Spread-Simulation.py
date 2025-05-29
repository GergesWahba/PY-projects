"""
Author: Gerges Wahba
Date: 05/13/2022
Purpose: Virus Spread Simulation Using Recursion and Iteration
"""

# ------------------------ Recursive Functions ------------------------ #

def new_infections_recursive(n: int) -> int:
    """
    Computes the number of newly infected individuals on day n using recursion.
    I(n) = I(n−1) + 2×I(n−2), with base cases I(1)=1, I(2)=2
    """
    if n == 1:
        return 1
    elif n == 2:
        return 2
    else:
        return new_infections_recursive(n - 1) + 2 * new_infections_recursive(n - 2)

def total_infected_recursive(n: int) -> int:
    """
    Computes the total number of infected individuals on day n using recursion.
    T(n) = T(n−1) + I(n), with base cases T(1)=1, T(2)=3
    """
    if n == 1:
        return 1
    elif n == 2:
        return 3
    else:
        return total_infected_recursive(n - 1) + new_infections_recursive(n)

# ------------------------ Iterative Function ------------------------ #

def total_infected_iterative(n: int) -> int:
    """
    Computes the total number of infected individuals on day n using iteration.
    """
    if n == 1:
        return 1
    elif n == 2:
        return 3

    prev1 = 1  # I(1)
    prev2 = 2  # I(2)
    total = 3  # T(2)
    
    for i in range(3, n + 1):
        current = prev2 + 2 * prev1  # I(n)
        total += current
        prev1, prev2 = prev2, current

    return total

# ------------------------ Main Simulation Loop ------------------------ #

def main():
    print("Virus Spread Simulation")
    print("-------------------------------------------------------------")

    while True:
        try:
            n = int(input("Enter the number of days (n ≥ 1): "))
            if n < 1:
                print("Please enter a valid number (n ≥ 1).")
                continue
        except ValueError:
            print("Invalid input. Please enter an integer.")
            continue

        # Calculate totals
        total_recursive = total_infected_recursive(n)
        total_iterative = total_infected_iterative(n)

        # Output results
        print(f"Recursive Approach: Total infected individuals on Day {n}: {total_recursive}")
        print(f"Iterative Approach: Total infected individuals on Day {n}: {total_iterative}")

        # Prompt to simulate again
        choice = input("Do you want to simulate again? (y/n): ").strip().lower()
        if choice != 'y':
            print("Simulation ended. Stay safe!")
            print("-------------------------------------------------------------")
            break

# ------------------------ Entry Point ------------------------ #

if __name__ == "__main__":
    main()