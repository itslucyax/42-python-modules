def ft_count_harvest_recursive() -> None:
    num = int(input("Days until harvest: "))

    def contar(dia_actual: int) -> None:
        if dia_actual > num:
            print("Harvest time!")
        else:
            print(f"Day {dia_actual}")
            contar(dia_actual + 1)
    contar(1)
