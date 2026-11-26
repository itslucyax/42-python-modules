from abc import ABC, abstractmethod

from .capability import Morphagon, Shiftling
from .creature import Creature, Flameling, Pyrodon


class CreatureFactory(ABC):
    """Abstract factory: creates a whole family of creatures."""

    @abstractmethod
    def create_base(self) -> Creature:
        """Create the base form of the family."""

    @abstractmethod
    def create_evolved(self) -> Creature:
        """Create the evolved form of the family."""


class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Flameling()

    def create_evolved(self) -> Creature:
        return Pyrodon()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Shiftling()

    def create_evolved(self) -> Creature:
        return Morphagon()
