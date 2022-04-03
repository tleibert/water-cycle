"""
Main file of the Water cycle simulation.
"""

from water_cycle.model import World


def run_game(starting_location, world: World):
    """
    Runs the game's main loop
    """

    current_location = starting_location
    while True:
        print(f"You are in {current_location}")
        user_input = input("What do you want to do?\n")
        if user_input is None or user_input.lower().startswith("q"):
            return


def main():
    """
    Starts the program
    """
    world = World.from_config("water_cycle/resources/world.yaml")
    print("Welcome to the Water Cycle!")
    print(world)
    start = world.random_location()
    print(f"You are starting in: {start.name}")
    print("You have the following fluxes available:")
    print(f"{start.outflows}")
    input()
    print("Goodbye!")


if __name__ == "__main__":
    main()
