def secure_archive(file_name: str, action: str = "read",
                   content: str | None = None) -> tuple[bool, str]:
    if action == "read":
        try:
            with open(file_name, "r") as archive:
                return (True, archive.read())
        except Exception as error:
            return (False, f"{error}")

    if action == "write":
        if content is None:
            return (False, "No content provided to write")
        try:
            with open(file_name, "w") as archive:
                archive.write(content)
            return (True, "Content successfully written to file")
        except Exception as error:
            return (False, f"{error}")

    return (False, "Unsupported action: use 'read' or 'write'")


def vault_security() -> None:
    print("=== Cyber Archives Security ===")
    print("")

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))
    print("")

    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/shadow"))
    print("")

    print("Using 'secure_archive' to read from a regular file:")
    result = secure_archive("ancient_fragment.txt")
    print(result)
    print("")

    print("Using 'secure_archive' to write previous content to a new file:")
    print(secure_archive("new_fragment.txt", "write", result[1]))


if __name__ == "__main__":
    vault_security()
