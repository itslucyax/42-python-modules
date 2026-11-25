import os
import sys
import sysconfig


def in_virtual_env() -> bool:
    """A venv is active when the running prefix differs from the base one."""
    return sys.prefix != sys.base_prefix


def show_open_laboratory() -> None:
    print("LABORATORY STATUS: You are working in the open")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You are in the global environment!")
    print("Every reagent you install here leaks into the whole system.")
    print()
    print("To seal the laboratory, run:")
    print()
    print("python3 -m venv lab_env")
    print("source lab_env/bin/activate # On Unix")
    print("lab_env\\Scripts\\activate # On Windows")
    print()
    print("Then run this program again.")


def show_sealed_laboratory() -> None:
    site_packages = sysconfig.get_paths()["purelib"]
    global_site_packages = sysconfig.get_paths(
        vars={"base": sys.base_prefix, "platbase": sys.base_prefix}
    )["purelib"]
    print("LABORATORY STATUS: The laboratory is sealed")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
    print(f"Environment Path: {sys.prefix}")
    print()
    print("SUCCESS: You are working in an isolated environment!")
    print("Safe to install reagents without affecting")
    print("the global system.")
    print()
    print("Reagent installation path:")
    print(site_packages)
    print()
    print("Global packages would live in:")
    print(global_site_packages)


def main() -> None:
    if in_virtual_env():
        show_sealed_laboratory()
    else:
        show_open_laboratory()


if __name__ == "__main__":
    main()
