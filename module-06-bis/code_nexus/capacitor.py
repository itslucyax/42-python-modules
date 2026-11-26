from ex3 import TransformCreatureFactory
from ex3.capability import TransformCapability
from ex3.creature import Creature


def test_capability(creature: Creature) -> None:
    print(creature.describe())
    print(creature.attack())
    if not isinstance(creature, TransformCapability):
        print(f"{creature.name} has no transform capability.")
        return
    print(creature.transform())
    print(creature.attack())
    print(creature.revert())


def main() -> None:
    print("Testing Creature with transform capability")
    factory = TransformCreatureFactory()
    print("base:")
    test_capability(factory.create_base())
    print("evolved:")
    test_capability(factory.create_evolved())


if __name__ == "__main__":
    main()
