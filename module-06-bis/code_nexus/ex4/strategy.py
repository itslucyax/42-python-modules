from abc import ABC, abstractmethod

from ex3.capability import TransformCapability
from ex3.creature import Creature


class InvalidStrategyError(Exception):
    """Raised when a strategy is used on an entity it is not valid for."""


class BattleStrategy(ABC):
    """Abstract strategy: how an entity behaves during its turn."""

    @abstractmethod
    def is_valid(self, entity: Creature) -> bool:
        """Tell whether the entity is suitable for this strategy."""

    @abstractmethod
    def act(self, entity: Creature) -> list[str]:
        """Play the entity's turn and return the resulting messages."""

    def _check(self, entity: Creature) -> None:
        if not self.is_valid(entity):
            raise InvalidStrategyError(
                f"{type(self).__name__} is not valid for {entity.name}"
            )


class NormalStrategy(BattleStrategy):
    """Suitable for any entity: simply attacks."""

    def is_valid(self, entity: Creature) -> bool:
        return True

    def act(self, entity: Creature) -> list[str]:
        self._check(entity)
        return [entity.attack()]


class AggressiveStrategy(BattleStrategy):
    """Suitable for transforming entities: transform, attack, revert."""

    def is_valid(self, entity: Creature) -> bool:
        return isinstance(entity, TransformCapability)

    def act(self, entity: Creature) -> list[str]:
        self._check(entity)
        if not isinstance(entity, TransformCapability):
            raise InvalidStrategyError(
                f"{type(self).__name__} is not valid for {entity.name}"
            )
        messages = [entity.transform()]
        try:
            messages.append(entity.attack())
        finally:
            messages.append(entity.revert())
        return messages
