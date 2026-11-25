import importlib
import importlib.metadata
import sys

REAGENTS: dict[str, str] = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
}


def get_version(name: str) -> str:
    """Import the reagent and return its installed version."""
    module = importlib.import_module(name)
    version = getattr(module, "__version__", None)
    if isinstance(version, str):
        return version
    return importlib.metadata.version(name)


def main() -> None:
    print("REAGENT STATUS: Loading reagents...")
    print()
    print("Checking dependencies:")
    missing: list[str] = []
    for name, description in REAGENTS.items():
        try:
            version = get_version(name)
        except ImportError:
            print(f"[MISSING] {name} - not installed")
            missing.append(name)
        else:
            print(f"[OK] {name} ({version}) - {description}")
    print()
    if missing:
        print("Some reagents are missing. Install them with:")
        print("  pip:    pip install -r ex0/requirements.txt")
        print("  Poetry: poetry install")
        print("Then run again (Poetry: poetry run python ex0/loading.py).")
        print()
    print("pip vs Poetry: requirements.txt declares what to install;")
    print("pip resolves it at install time.")
    print("pyproject.toml declares the same constraints, and Poetry pins")
    print("the resolved versions in poetry.lock so every install is")
    print("identical.")
    print()
    if missing:
        print(f"Missing reagents: {', '.join(missing)}")
        sys.exit(1)
    print("All reagents present and accounted for.")


if __name__ == "__main__":
    main()
