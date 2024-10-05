import os
import sys
from enum import Enum


class CommandType(Enum):
    REVERSE = "reverse"
    COPY = "copy"
    DUPLICATE_CONTENTS = "duplicate_contents"
    REPLACE_STRING = "replace_string"


def exit_and_output_error(message: str) -> None:
    sys.stderr.write(f"Error: {message}\n")
    sys.exit(1)


def get_valid_command_type() -> CommandType:
    if len(sys.argv) < 2:
        exit_and_output_error("Please specify command type")

    try:
        return CommandType(sys.argv[1])
    except ValueError:
        command_types = ", ".join([command.value for command in CommandType])

        exit_and_output_error(f"Please specify one of the commands [{command_types}]")


def check_if_exists_file(*file_paths: str):
    for file_path in file_paths:
        if os.path.isfile(file_path):
            return

        exit_and_output_error(f"Invalid file path: {file_path}")


def cast_to_positive_number(value: str, arg_name: str) -> int:
    try:
        int_value = int(value)

        if int_value > 0:
            return int_value

        raise ValueError
    except ValueError:
        exit_and_output_error(f"{arg_name} must be a positive number")


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


def check_args_count(args: list[str], expect_count: int) -> None:
    if len(args) < expect_count:
        exit_and_output_error("Missing argument")


def reverse(args: list[str]) -> None:
    check_args_count(args, 2)

    input_path, output_path = args

    check_if_exists_file(input_path)

    with open(input_path, "r") as f:
        contents = f.read()

    with open(output_path, "w") as f:
        f.write(contents[::-1])


def copy(args: list[str]) -> None:
    check_args_count(args, 2)

    input_path, output_path = args

    check_if_exists_file(input_path)

    with open(input_path, "r") as f:
        contents = f.read()

    with open(output_path, "w") as f:
        f.write(contents)


def duplicate_contents(args: list[str]) -> None:
    check_args_count(args, 2)

    input_path, str_n = args

    check_if_exists_file(input_path)

    n = cast_to_positive_number(str_n, arg_name="n")

    with open(input_path, "r+") as f:
        f.write(f.read() * n)


def replace_string(args: list[str]) -> None:
    check_args_count(args, 3)

    input_path, needle, new_string = args

    check_if_exists_file(input_path)

    with open(input_path, "r") as f:
        contents = f.read()

    with open(input_path, "w") as f:
        f.write(contents.replace(needle, new_string))


def main() -> None:
    command_type = get_valid_command_type()

    exec_command(command_type, sys.argv[2::])

    sys.exit(0)


if __name__ == "__main__":
    main()
