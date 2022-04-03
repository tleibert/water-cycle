"""
Module providing components of the water cycle. The water cycle
is composed of Locations, where water can reside for a period of time,
and Fluxes, which are transitions of water between Locations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Sequence


class Component(ABC):
    """
    Generic component of the water cycle.
    """

    @abstractmethod
    def __init__(
        self,
        name: str,
        description: str = "No long-form description available.\n",
        amount: Optional[float] = None,
        variance: Optional[float] = None,
    ):
        self._name = name
        self._description = description
        self._amount = amount
        self._variance = variance

    @property
    def name(self) -> str:
        """
        Returns the short name of this part of the water cycle
        """
        return self._name

    @property
    def description(self) -> str:
        """
        Returns the long-form description of this part of the water cycle
        """
        return self._description

    @property
    def info(self) -> Optional[str]:
        """
        Returns the amount +- variance pair describing
        this component's water content.
        """
        if self._amount is None or self._variance is None:
            return None

        return f"{self._amount} ± {self._variance}%"

    @abstractmethod
    def __repr__(self) -> str:
        pass


class Flux(Component):
    """
    Represents a flux in the Water cycle. A flux is a
    transition from one Location to another.
    Flux names don't have to be unique.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        source: "Location",
        destination: "Location",
        description: str = "No long-form description available.\n",
        amount: Optional[float] = None,
        variance: Optional[float] = None,
    ):
        super().__init__(name, description, amount=amount, variance=variance)
        self._source = source
        self._destination = destination

    @property
    def source(self) -> "Location":
        """
        Source location of the flux
        """
        return self._source

    @property
    def destination(self) -> "Location":
        """
        Destination location of the flux
        """
        return self._destination

    def __repr__(self) -> str:
        return f"Flux({self._name}: {self._source.name} -> {self._destination.name})"


class Location(Component):
    """
    Generic location water can occupy.
    Location names must be unique.
    """

    def __init__(
        self,
        name: str,
        description: str = "No long-form description available.\n",
        amount: Optional[float] = None,
        variance: Optional[float] = None,
    ):
        """
        Creates a new Location
        """
        super().__init__(name, description, amount, variance)
        self._outflows: List["Flux"] = []
        self._inflows: List["Flux"] = []

    @property
    def outflows(self) -> Sequence["Flux"]:
        """
        Returns an immutable view of the outflows from this Location
        """
        return tuple(self._outflows)

    def add_outflow(self, outflow: "Flux"):
        """
        Register an outflow from this Location
        """
        self._outflows.append(outflow)

    @property
    def inflows(self) -> Sequence["Flux"]:
        """
        Returns an immutable view of the inflows to this Location
        """
        return tuple(self._inflows)

    def add_inflow(self, inflow: "Flux"):
        """
        Register an inflow to this location
        """
        self._inflows.append(inflow)

    def __repr__(self) -> str:
        return f"Location(name: {self._name}, amount: {self._amount}, variance: {self._variance}%"
