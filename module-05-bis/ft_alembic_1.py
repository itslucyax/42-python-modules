import alchemy

print("=== Alembic 1 ===")
print("Accessing the lab through 'import alchemy'")
print("Testing create_air:", alchemy.create_air())
print("Now trying to reach create_earth through the package interface:")
try:
    print(alchemy.create_earth())
except AttributeError as error:
    print(f"Caught AttributeError: {error}")
