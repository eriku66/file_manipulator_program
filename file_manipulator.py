import os
import sys
from enum import Enum


class CommandType(Enum):
    REVERSE = "reverse"
    COPY = "copy"
    DUPLICATE_CONTENTS = "duplicate_contents"
    REPLACE_STRING = "replace_string"


def get_valid_command_type() -> CommandType:
    try:
        return CommandType(sys.argv[1])
    except ValueError:
        command_types = ", ".join([command.value for command in CommandType])

        sys.stderr.write(f"Please specify one of the commands [{command_types}]")


def check_if_exists_file(*file_paths: str):
    for file_path in file_paths:
        if os.path.isfile(file_path):
            return

        sys.stderr.write(f"Invalid file path: {file_path}")

        raise ValueError


def cast_to_positive_number(value: str, arg_name: str) -> int:
    try:
        return int(value)
    except ValueError:
        sys.stderr.write(f"{arg_name} must be a positive number")

        raise ValueError


def exec_command(command_type: CommandType, args: list[str]) -> None:
    match command_type:
        case CommandType.REVERSE:
            reverse(args)
        case CommandType.COPY:
            copy(args)
        case CommandType.DUPLICATE_CONTENTS:
            duplicate_contents(args)
        case CommandType.REPLACE_STRING:
            replace_string(args)


def reverse(args: list[str]) -> None:
    input_path = args[0]

    check_if_exists_file(input_path)

    output_path = args[1]

    with open(input_path, "r") as f:
        contents = f.read()

    with open(output_path, "w") as f:
        f.write(contents[::-1])


def copy(args: list[str]) -> None:
    input_path = args[0]

    check_if_exists_file(input_path)

    output_path = args[1]

    with open(input_path, "r") as f:
        contents = f.read()

    with open(output_path, "w") as f:
        f.write(contents)


def duplicate_contents(args: list[str]) -> None:
    input_path = args[0]

    check_if_exists_file(input_path)

    n = cast_to_positive_number(args[1], arg_name="n")

    with open(input_path, "r+") as f:
        f.write(f.read() * n)


def replace_string(args: list[str]) -> None:
    input_path = args[0]

    check_if_exists_file(input_path)

    needle = args[1]
    new_string = args[2]

    with open(input_path, "r") as f:
        contents = f.read()

    with open(input_path, "w") as f:
        f.write(contents.replace(needle, new_string))


def main() -> None:
    try:
        command_type = get_valid_command_type()

        exec_command(command_type, sys.argv[2::])

        sys.exit(0)
    except ValueError:
        sys.exit(1)


if __name__ == "__main__":
    main()
