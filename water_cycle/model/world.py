"""
Represents the World that contains the water cycle.
"""

import random
from typing import List, Mapping, Optional

import yaml

from water_cycle.model.components import Flux, Location


class World:
    """
    Represents the world that the water cycle is in.
    """

    def __init__(
        self,
        locations: List[Location],
        fluxes: List[Flux],
        location_name_map: Mapping[str, Location],
    ):
        self._locations = locations
        self._fluxes = fluxes
        self._location_name_map = location_name_map

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

        # generate fluxes, and attach locations to them - each flux contains a list
        # of sources and destinations, we need to make a Flux object for each
        # unique combination of source and destination, where the two are not the same.
        fluxes = []
        for flux_src in data["world"]["fluxes"]:
            # grab the location objects corresponding to
            sources = flux_src["sources"]
            destinations = flux_src["destinations"]

            for source_str in sources:
                for destination_str in destinations:
                    # no flows should go from a place to itself, unless overridden
                    if source_str == destination_str and not flux_src.get(
                        "self_reference"
                    ):
                        continue

                    source = locations[source_str]
                    destination = locations[destination_str]

                    flux = {}
                    for key in ["name", "amount", "variance", "description"]:
                        flux[key] = flux_src.get(key)
                    # create the Flux object
                    flux["source"] = source
                    flux["destination"] = destination
                    new_flux = Flux(**flux)

                    # add the new Flux object to the source location's outflow list
                    # and to the destination location's inflow list
                    source.add_outflow(new_flux)
                    destination.add_inflow(new_flux)
                    fluxes.append(new_flux)

        return cls(list(locations.values()), fluxes, locations)

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

    def get_location_by_name(self, name: str) -> Optional[Location]:
        """
        Returns the location with the given name from the world.
        """

        return self._location_name_map.get(name)

    def __repr__(self) -> str:
        return "World(\n" + "    \n".join(repr(flux) for flux in self._fluxes) + "\n)"
