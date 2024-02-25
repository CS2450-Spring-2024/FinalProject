from uvsim.constants import MEM_SIZE, TERMINAL_WORD


def get_program_from_file(path) -> list[int]:
    """Get program from file"""

    with open(path, "r") as in_file:
        program = in_file.read()
    program = parse_str(program)
    return program

def try_parse_cli(program, tries=0):
    word = input(f"{len(program)} ? ")
    try:
        word = parse_word(word, len(program))
    except ValueError:
        print(f'Could not parse "{word}", try again.')
        return try_parse_cli(program, tries + 1)

    return word

def get_program_from_cli() -> list[int]:
    """Get program from CLI"""

    program = []
    while True:
        word = try_parse_cli(program)
        program.append(word)

        if word == TERMINAL_WORD:  # Terminate if -99999
            program = validate_program(program)

            return program

        if len(program) > MEM_SIZE:
            raise AssertionError(
                f"Invalid program, must be {MEM_SIZE} lines or less!\nProgram:{program}"
            )


def parse_word(word: str, addr: int) -> int:
    try:
        val = int(word)
    except ValueError as e:
        raise ValueError(f"Could not parse ${addr}: {word}") from e
    return val


def parse_str(program: str) -> int:
    """Returns an validated program from a given string. If a program is invalid, this throws an AssertionError"""
    program = program.strip()
    program = [parse_word(word, i) for i, word in enumerate(program.split("\n"))]

    program = validate_program(program)

    return program


def validate_program(program: list[int]) -> list[int]:
    assert (
        program[-1] == TERMINAL_WORD
    ), f"Invalid program, must be terminated with {TERMINAL_WORD}!\nProgram:{program}"
    program.pop() # pop TERMINAL_WORD

    assert (
        len(program) <= MEM_SIZE
    ), f"Invalid program, must be {MEM_SIZE} lines or less!\nProgram:{program}"

    program.extend([0] * MEM_SIZE)
    program = program[:MEM_SIZE + 1]
    return program

def save_memory(memory: list[int], path: str):
    end_idx = MEM_SIZE
    for idx in range(len(memory) - 1, -1, -1):
        if memory[idx] != 0:
            end_idx = idx
            break

    with open(path, 'w') as file:
        lines = memory[:end_idx + 1]
        lines.append(-99999)
        output = '\n'.join(map(lambda word: str(word), lines))
        file.write(output)
