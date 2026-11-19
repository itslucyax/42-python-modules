import random


def gen_player_achievements(achievements: list[str]) -> set[str]:
    selection = random.sample(achievements, random.randint(15, 25))
    return set(selection)


def achievement_tracker() -> None:
    achievements = [
        "Crafting Genius", "World Savior", "Master Explorer",
        "Collector Supreme", "Untouchable", "Boss Slayer",
        "Strategist", "Speed Runner", "Survivor",
        "Treasure Hunter", "Unstoppable", "Hidden Path Finder",
        "First Steps", "Sharp Mind", "Lone Wolf",
        "Team Player", "Night Owl", "Early Bird",
        "Lucky Strike", "Iron Will", "Quick Draw",
        "Dungeon Master", "Pet Whisperer", "Gold Hoarder",
        "Master Chef", "Sky Walker", "Deep Diver",
        "Monster Hunter", "Puzzle Solver", "Legend",
        "Pacifist", "Berserker", "Merchant King",
        "Grand Architect", "Time Traveler", "Ghost",
        "Marathoner", "Sharpshooter", "Alchemist", "Trailblazer"]
    all_achievements = set(achievements)

    alice = gen_player_achievements(achievements)
    bob = gen_player_achievements(achievements)
    charlie = gen_player_achievements(achievements)
    dylan = gen_player_achievements(achievements)

    print(f"Player Alice: {alice}")
    print(f"Player Bob: {bob}")
    print(f"Player Charlie: {charlie}")
    print(f"Player Dylan: {dylan}\n")

    distinct = alice.union(bob, charlie, dylan)
    common = alice.intersection(bob, charlie, dylan)

    print(f"All distinct achievements: {distinct}\n")
    print(f"Common achievements: {common}\n")

    print(f"Only Alice has: {alice.difference(bob, charlie, dylan)}")
    print(f"Only Bob has: {bob.difference(alice, charlie, dylan)}")
    print(f"Only Charlie has: {charlie.difference(alice, bob, dylan)}")
    print(f"Only Dylan has: {dylan.difference(alice, bob, charlie)}\n")

    print(f"Alice is missing: {all_achievements.difference(alice)}")
    print(f"Bob is missing: {all_achievements.difference(bob)}")
    print(f"Charlie is missing: {all_achievements.difference(charlie)}")
    print(f"Dylan is missing: {all_achievements.difference(dylan)}")


if __name__ == "__main__":
    print("=== Achievement Tracker System ===\n")
    achievement_tracker()
