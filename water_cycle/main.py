"""
Main file of the Water cycle simulation.
"""

import sys

from rich.console import Console
from PyInquirer import prompt

from water_cycle.model import World, Location, Flux

console = Console()


def ask_next_action():
    """
    Top-level prompt for a step through the game.
    The actions a user can take at the top-level are viewing
    the possible outflows from their stage in the water cycle,
    learning more about their stage in the water cycle, and
    exiting the application.
    """

    action_prompt = {
        "type": "list",
        "name": "action",
        "message": "What would you like to do?",
        "choices": ["view description", "choose outflow", "quit"],
    }
    answers = prompt(action_prompt)
    return answers["action"]


def view_description(location: Location):
    """
    Gets the detailed information
    """
    console.print(f"[green]{location.name}[/green]")
    data = location.info
    if data:
        console.print(
            f"Total pool size and certainty: [cyan]{data}[/cyan] "
            "[dim](in 1000s of cubic kilometers of water)[/dim]\n"
        )

    console.print("Description:")
    console.print(location.description)
    input()


def choose_outflow(location: Location) -> Flux:
    fluxes = location.outflows
    flux_name_map = {flux.name: flux for flux in fluxes}

    flux_prompt = {
        "type": "list",
        "name": "flux",
        "message": f"Possible outflows from {location.name}:",
        "choices": list(flux_name_map.keys()),
    }

    answers = prompt(flux_prompt)
    return flux_name_map[answers["flux"]]


def game_step(world: World, location: Location) -> Location:
    """
    Runs an iteration the game's main loop.

    Returns true if the game should step again
    """

    print(f"Your location: {location.name}")
    action = ask_next_action()
    if action == "quit":
        print("Goodbye!")
        sys.exit(0)
    elif action == "view description":
        view_description(location)
    elif action == "choose outflow":
        # get the flux corresponding to the chosen outflow
        flux = choose_outflow(location)

        
    else:
        raise ValueError(f"Unknown action {action}")

    return location


def start_interactive(world: World):
    """
    Runs the interactive loop of the simulation.
    """

    location = world.random_location()

    while True:
        new_location = game_step(world, location)
        if new_location is not location:
            console.clear()
            location = new_location


def main():
    """
    Starts the program
    """
    world = World.from_config("water_cycle/resources/world.yaml")
    console.print("Welcome to the Water Cycle!")

    try:
        start_interactive(world)
    except EOFError:
        pass  # exit gracefully

    print("Goodbye!")


if __name__ == "__main__":
    main()
