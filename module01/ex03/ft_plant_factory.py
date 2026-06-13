#!/usr/bin/env python3

class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

    def grow(self):
        self.height += 2.5
        print(f"{self.name} grew! New height: {self.height}cm")

    def show(self):
        print(f"| {self.name:<15} | {self.height:<12} | {self.age:<10} |")

if  __name__ == "__main__":
    plant1 = Plant("Ferny", 12.5, 5)
    plant2 = Plant("Spike the Cactus", 5.0, 20)
    plant3 = Plant("Sunny Sunflower", 45.0, 15)
    plant4 = Plant("Bella Orchid", 22.1, 8)
    plant5 = Plant("Ivy", 30.0, 12)

garden_factory = [plant1, plant2, plant3, plant4, plant5]

print("-" * 49)
print(f"| {'Plant Name':<15} | {'Height (cm)':<12} | {'Age (days)':<10} |")
print("-" * 49)

for plant in garden_factory:
    plant.display_info()

print("-" * 49)

print("\nTesting immediate functionality (Triggering grow() on Ferny):")
plant1.grow()
