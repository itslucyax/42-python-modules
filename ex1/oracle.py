import os
import sys

try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False

HERE = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(HERE, ".env")
GITIGNORE = os.path.join(HERE, ".gitignore")
KEYS = ["MATRIX_MODE", "DATABASE_URL", "API_KEY", "LOG_LEVEL",
        "ZION_ENDPOINT"]
SECRET_KEYS = ["DATABASE_URL", "API_KEY"]
DEFAULTS: dict[str, str] = {
    "MATRIX_MODE": "development",
    "LOG_LEVEL": "DEBUG",
}
PROD_DEFAULTS: dict[str, str] = {"LOG_LEVEL": "WARNING"}


def load_config() -> tuple[dict[str, str | None], list[str]]:
    """Return the configuration and a list of warnings."""
    warnings: list[str] = []
    if not HAS_DOTENV:
        warnings.append("python-dotenv not installed: .env ignored "
                        "(pip install -r ex1/requirements.txt)")
    elif os.path.exists(ENV_FILE):
        # override=False: real environment variables win over .env
        load_dotenv(ENV_FILE, override=False)
    else:
        warnings.append("No .env file found (copy ex1/.env.example)")
    config: dict[str, str | None] = {}
    for key in KEYS:
        config[key] = os.environ.get(key)
    mode = config["MATRIX_MODE"]
    if mode is None:
        warnings.append("MATRIX_MODE missing, using 'development'")
        config["MATRIX_MODE"] = DEFAULTS["MATRIX_MODE"]
    elif mode not in ("development", "production"):
        warnings.append(f"Unknown MATRIX_MODE '{mode}', using 'development'")
        config["MATRIX_MODE"] = DEFAULTS["MATRIX_MODE"]
    if config["LOG_LEVEL"] is None:
        if config["MATRIX_MODE"] == "production":
            config["LOG_LEVEL"] = PROD_DEFAULTS["LOG_LEVEL"]
        else:
            config["LOG_LEVEL"] = DEFAULTS["LOG_LEVEL"]
        warnings.append(f"LOG_LEVEL missing, using {config['LOG_LEVEL']}")
    for key in ("DATABASE_URL", "API_KEY", "ZION_ENDPOINT"):
        if config[key] is None:
            warnings.append(f"{key} is not configured")
    return config, warnings


def describe(config: dict[str, str | None]) -> list[str]:
    production = config["MATRIX_MODE"] == "production"
    if config["DATABASE_URL"] is None:
        database = "Not configured"
    elif production:
        database = "Connected to production cluster"
    else:
        database = "Connected to local instance"
    api = ("Authenticated" if config["API_KEY"] is not None
           else "Not authenticated")
    remote = "Online" if config["ZION_ENDPOINT"] is not None else "Offline"
    return [
        f"Mode: {config['MATRIX_MODE']}",
        f"Database: {database}",
        f"API Access: {api}",
        f"Log Level: {config['LOG_LEVEL']}",
        f"Remote Network: {remote}",
    ]


def source_has_no_secrets(config: dict[str, str | None]) -> bool:
    with open(os.path.abspath(__file__), encoding="utf-8") as source:
        code = source.read()
    for key in SECRET_KEYS:
        value = config[key]
        if value and value in code:
            return False
    return True


def env_file_is_ignored() -> bool:
    try:
        with open(GITIGNORE, encoding="utf-8") as ignore:
            lines = [line.strip() for line in ignore]
    except OSError:
        return False
    return ".env" in lines


def main() -> None:
    print("ORACLE STATUS: Consulting the configuration...")
    print()
    config, warnings = load_config()
    print("Configuration loaded:")
    for line in describe(config):
        print(line)
    print()
    print("Configuration security check:")
    ok = source_has_no_secrets(config)
    print("[OK]" if ok else "[KO]", "No hardcoded secrets detected")
    ignored = env_file_is_ignored()
    print("[OK]" if ignored else "[KO]", ".env file properly ignored by git")
    print("[OK] Production overrides available")
    print("     (environment variables take precedence over .env)")
    if warnings:
        print()
        for warning in warnings:
            print(f"WARNING: {warning}")
    production_missing = [
        key for key in SECRET_KEYS
        if config["MATRIX_MODE"] == "production" and config[key] is None
    ]
    if production_missing:
        print()
        print("ERROR: production requires " + ", ".join(production_missing))
        sys.exit(1)
    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
