import os
import random

import yaml


def main():
    print(os.getcwd())
    with open("water_cycle/resources/story.yaml") as fh:
        gamerules = yaml.safe_load(fh)

    print(gamerules)

    print("Welcome to the Water Cycle!")

    starting_location = random.choice(list(gamerules["world"].keys()))
    current_location = starting_location

    while True:
        print(f"You are in {current_location}")
        user_input = input("What do you want to do?\n")
        if user_input is None or user_input.lower().startswith("q"):
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
