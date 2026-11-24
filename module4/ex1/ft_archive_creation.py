import sys


def text_recovery() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return

    file_name = sys.argv[1]
    print(f"Accessing file '{file_name}'")

    try:
        file = open(file_name, "r")
        content = file.read()
        file.close()
    except Exception as e:
        print(f"Error opening file '{file_name}': {e}")
        return

    print("---")
    print(content, end="")
    print("---")
    print(f"File '{file_name}' closed.\n")

    print("Transform data:\n---")
    new_content = ""
    for line in content.splitlines():
        new_line = f"{line}#"
        new_content += new_line + "\n"
        print(new_line)
    print("---")

    new_name = input("Enter new file name (or empty): ").strip()
    if new_name:
        print(f"Saving data to '{new_name}'")
        try:
            new_file = open(new_name, "w")
            new_file.write(new_content)
            new_file.close()
            print(f"Data saved in file '{new_name}'.")
        except Exception as e:
            print(f"Error opening file '{new_name}': {e}")
            print("Data not saved.")
    else:
        print("Not saving data.")


if __name__ == "__main__":
    print("=== Cyber Archives Recovery & Preservation ===")
    text_recovery()
