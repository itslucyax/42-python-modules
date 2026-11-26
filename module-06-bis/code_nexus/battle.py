from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())


def test_battle(factory_a: CreatureFactory,
                factory_b: CreatureFactory) -> None:
    print("Testing battle")
    fighter_a = factory_a.create_base()
    fighter_b = factory_b.create_base()
    print(fighter_a.describe())
    print("vs.")
    print(fighter_b.describe())
    print("fight!")
    print(fighter_a.attack())
    print(fighter_b.attack())


def main() -> None:
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()
    test_factory(flame_factory)
    print()
    test_factory(transform_factory)
    print()
    test_battle(flame_factory, transform_factory)


if __name__ == "__main__":
    main()
