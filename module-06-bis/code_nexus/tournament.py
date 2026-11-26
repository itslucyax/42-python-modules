from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
from ex4 import (
    AggressiveStrategy,
    BattleStrategy,
    InvalidStrategyError,
    NormalStrategy,
)


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    """Every opponent faces each other one once, using its own strategy."""
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    fighters = [(factory.create_base(), strategy)
                for factory, strategy in opponents]
    try:
        for entity, strategy in fighters:
            if not strategy.is_valid(entity):
                raise InvalidStrategyError(
                    f"{type(strategy).__name__} is not valid for "
                    f"{entity.name}"
                )
        for i in range(len(fighters)):
            for j in range(i + 1, len(fighters)):
                entity_a, strategy_a = fighters[i]
                entity_b, strategy_b = fighters[j]
                print("\n* Battle *")
                print(entity_a.describe())
                print(f" Strategy: {type(strategy_a).__name__}")
                print("vs.")
                print(entity_b.describe())
                print(f" Strategy: {type(strategy_b).__name__}")
                print("now fight!")
                for message in strategy_a.act(entity_a):
                    print(message)
                for message in strategy_b.act(entity_b):
                    print(message)
    except InvalidStrategyError as error:
        print(f"\nBattle error, aborting tournament: {error}")


def main() -> None:
    flame = FlameFactory()
    transform = TransformCreatureFactory()
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()

    print("Tournament 0 (basic)")
    print("[ (Flame+Normal), (Transform+Normal) ]")
    battle([(flame, normal), (transform, normal)])

    print("\nTournament 1 (error)")
    print("[ (Flame+Aggressive), (Transform+Normal) ]")
    battle([(flame, aggressive), (transform, normal)])

    print("\nTournament 2 (multiple)")
    print("[ (Transform+Aggressive), (Flame+Normal), (Transform+Normal) ]")
    battle([(transform, aggressive), (flame, normal), (transform, normal)])


if __name__ == "__main__":
    main()
