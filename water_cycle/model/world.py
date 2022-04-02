"""
Represents the World that contains the water cycle.
"""

import random
from typing import List

import yaml

from water_cycle.model.components import Flux, Location


class World:
    """
    Represents the world that the water cycle is in.
    """

    def __init__(self, locations: List[Location], fluxes: List[Flux]):
        self._locations = locations
        self._fluxes = fluxes

    @classmethod
    def _from_config(cls, filename: str) -> "World":
        """
        Creates a world from a config file, without error handling.
        """
        with open(filename, encoding="utf-8") as world_file:
            data = yaml.safe_load(world_file)

        # generate map of location name strings to location objects
        locations = {
            location["name"]: Location(**location)
            for location in data["world"]["locations"]
        }

        # generate fluxes, and attach locations to them
        fluxes = []
        for flux in data["world"]["fluxes"]:
            # grab the location objects corresponding to
            source = locations[flux["source"]]
            destination = locations[flux["destination"]]

            # create the Flux object
            flux["source"] = source
            flux["destination"] = destination
            new_flux = Flux(**flux)

            # add the new Flux object to the source location's outflow list
            # and to the destination location's inflow list
            source.add_outflow(new_flux)
            destination.add_inflow(new_flux)
            fluxes.append(new_flux)

        return cls(list(locations.values()), fluxes)

    @classmethod
    def from_config(cls, filename: str) -> "World":
        """
        Generates a world from a config file.
        """
        try:
            return cls._from_config(filename)
        except KeyError as error:
            raise ValueError("Invalid world file format!") from error
        except IOError as error:
            raise ValueError(f"Couldn't find or read world file {filename}") from error

    def random_location(self) -> Location:
        """
        Returns a random location in the world. Locations
        are all weighted equally for selection.

        (Otherwise you'd start in the ocean almost every time)
        """

        return random.choice(self._locations)

    def __repr__(self) -> str:
        return "World(\n" + "    \n".join(repr(flux) for flux in self._fluxes) + "\n)"