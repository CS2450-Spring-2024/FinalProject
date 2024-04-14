from tkinter import filedialog, messagebox
from uvsim.constants import FOURDP_FILETYPES, FOURDP_WORD_SIZE, MEM_SIZE, WORD_SIZE, TERMINAL_WORD, WORKING_DIR
from uvsim.opcodes import OPCODES

def word_to_op_data_4dp(word: int) -> tuple[int, int]:
    """
    Purpose:
        pulls opcode and data from an instruction line.
    Input Parameters:
        line: An instruction line from memory.
    Return Value:
        A tuple that holds the opcode and data.
    Pre-conditions:
        The line must be a valid instruction line.
    Post-conditions:
        None.
    """
    data = word % FOURDP_WORD_SIZE
    opcode = (word - data)
    return (opcode, data)

def word_to_op_data(word: int) -> tuple[int, int]:
    """
    Purpose:
        pulls opcode and data from an instruction line.
    Input Parameters:
        line: An instruction line from memory.
    Return Value:
        A tuple that holds the opcode and data.
    Pre-conditions:
        The line must be a valid instruction line.
    Post-conditions:
        opcode and data are extracted from the line.
    """
    data = word % WORD_SIZE
    opcode = (word - data)
    return (opcode, data)

def get_program_from_file(path, check_6dp=True) -> list[int]:
    """
    Purpose:
        Get program from file.
    Input Parameters:
        path: The path to the file.
    Return Value:
        The program.
    Pre-conditions:
        The file must exist and be readable.
    Post-conditions:
        The program is returned.
    """

    with open(path, "r") as in_file:
        program = in_file.read()
    program = parse_str(program, check_6dp)
    return program

def try_parse_cli(program, tries=0):
    """
    Purpose:
        Try to parse a word from the command line.
    Input Parameters:
        program: The program so far.
        tries: The number of tries so far.
    Return Value:
        The parsed word.
    Pre-conditions:
        A valid program must be passed.
    Post-conditions:
        The word is parsed.
    """
    word = input(f"{len(program)} ? ")
    try:
        word = parse_word(word, len(program))
    except ValueError:
        print(f'Could not parse "{word}", try again.')
        return try_parse_cli(program, tries + 1)

    return word

def get_program_from_cli() -> list[int]:

    """
    Purpose:
        Get program from command line.
    Input Parameters:
        None.
    Return Value:
        The program.
    Pre-conditions:
        cli must be enabled.
    Post-conditions:
        The program is returned.
    """

    program = []
    while True:
        word = try_parse_cli(program)
        program.append(word)

        if word == TERMINAL_WORD:  # Terminate if -99999
            program = validate_program(program)

            return program

        if len(program) > WORD_SIZE:
            raise AssertionError(
                f"Invalid program, must be {MEM_SIZE} lines or less!\nProgram:{program}"
            )


def parse_word(word: str, addr: int) -> int:
    """
    Purpose:
        Parse a word from the command line.
    Input Parameters:
        word: The word to parse.
        addr: The address of the word.
    Return Value:
        The parsed word.
    Pre-conditions:
        The word must be a valid word.
    Post-conditions:
        The word is parsed.
    """
    try:
        val = int(word)
    except ValueError as e:
        raise ValueError(f"Could not parse ${addr}: {word}") from e
    return val


def parse_str(program: str, check_6dp=True) -> int:
    """
    Purpose:
        Returns an validated program from a given string. If a program is invalid, this throws an AssertionError
    Input Parameters:
        program: The program to parse.
    Return Value:
        The parsed program.
    Pre-conditions:
        The program must be a valid program.
    Post-conditions:
        The program is parsed.
    """
    program = program.strip()
    program = [parse_word(word, i) for i, word in enumerate(program.split("\n"))]

    program = validate_program(program, check_6dp)

    return program


def validate_program(program: list[int], check_6dp=True) -> list[int]:
    """
    Purpose:
        Validates a program. If the program is invalid, this throws an AssertionError
    Input Parameters:
        program: The program to validate.
    Return Value:
        The validated program.
    Pre-conditions:
        The program must be a valid program.
    Post-conditions:
        The program is validated.
    """
    assert (
        program[-1] == TERMINAL_WORD
    ), f"Invalid program, must be terminated with {TERMINAL_WORD}!\nProgram: {program}"
    program.pop() # pop TERMINAL_WORD

    assert (
        len(program) <= MEM_SIZE
    ), f"Invalid program, must be {MEM_SIZE} lines or less!\nProgram: {program}"

    if check_6dp:
        prog_type = classify_program(program)
        assert (
            prog_type == "6dp"
        ), f"Program type was {prog_type}, but only 6dp programs are accepted. Please use the migration tool or check your syntax."

    program.extend([0] * MEM_SIZE)
    program = program[:MEM_SIZE]
    return program


def save_memory(memory: list[int], path: str):
    """
    Purpose:
        Save memory to a file.
    Input Parameters:
        memory: The memory to save.
        path: The path to save the memory to.
    Return Value:
        None.
    Pre-conditions:
        The memory must be a valid memory.
    Post-conditions:
        The memory is saved to the file.
    """
    end_idx = MEM_SIZE
    for idx in range(len(memory) - 1, -1, -1):
        if memory[idx] != 0:
            end_idx = idx
            break

    with open(path, 'w') as file:
        lines = memory[:end_idx + 1]
        lines.append(TERMINAL_WORD)
        output = '\n'.join(map(lambda word: str(word), lines))
        file.write(output)


def fourdp_word_to_sixdp_word(word: int) -> int:
    """
    Purpose:
        Converts a 4dp instruction word to a 6dp instruction word
    Input Parameters:
        word: The 4dp instruction word
    Return Value:
        The 6dp instruction word
    Pre-conditions:
        Requires that word is a valid 4dp instruction word
    Post-conditions:
        The 4dp instruction word is converted to a 6dp instruction word
    """
    scaling_factor = WORD_SIZE // FOURDP_WORD_SIZE
    op, data = word_to_op_data_4dp(word)
    return op * scaling_factor + data

def convert_4dp_prog_to_6dp(program: list[int]) -> list[int]:
    """
    Purpose:
        Converts a 4dp program to a 6dp program
    Input Parameters:
        program: The 4dp program
    Return Value:
        The 6dp program
    Pre-conditions:
        Requires that program is a valid 4dp program
    Post-conditions:
        The 4dp program is converted to a 6dp program
    """
    return [fourdp_word_to_sixdp_word(word) for word in program]


def convert_4dp_file_to_6dp(filepath: str):
    """
    Purpose:
        Converts a 4dp program file to a 6dp program file
    Input Parameters:
        filepath: The path to the 4dp program file
    Return Value:
        None
    Pre-conditions:
        Requires that the file at filepath is a valid 4dp program
    Post-conditions:
        The 4dp program is converted to a 6dp program and saved to a new file
    """
    new_filepath = filepath.replace(".4dp", ".6dp")

    four_prog = get_program_from_file(file_path, check_6dp=False)
    six_prog = convert_4dp_prog_to_6dp(four_prog)
    save_memory(six_prog, new_filepath)


def classify_program(program: list[int]) -> str:
    """
    Classifies a program as 4dp or 6dp.

    Returns "4dp" if the program is a 4dp program
    Returns "6dp" if the program is a 4dp program
    Returns "unknown" if the function was inconclusive

    How it works:
    We iterate through all words in a program.
    For every word, we check if the opcode is a valid 4/6 digit opcode, and it may be unknown as well.
    If it's 4/6, then we assume it's a 4/6 digit program.
    If not, we move on to the next word.
    If all words in a program are unknown, we return unknown.
    """
    scaling_factor = WORD_SIZE // FOURDP_WORD_SIZE

    fourdp_opcodes = list(map(lambda op: op // scaling_factor, OPCODES))
    sixdp_opcodes = OPCODES

    for word in program:
        op6, _ = word_to_op_data(word)
        op4, _ = word_to_op_data_4dp(word)

        if op4 in fourdp_opcodes and op6 not in sixdp_opcodes:
            return "4dp"
        elif op4 not in fourdp_opcodes and op6 in sixdp_opcodes:
            return "6dp"

    return "unknown"

def convert_dialog():
    file_path = filedialog.askopenfilename(title="Open", filetypes=FOURDP_FILETYPES, initialdir=WORKING_DIR)

    if file_path:
        try:
            # Open and read the file
            convert_4dp_file_to_6dp(file_path)

        except Exception as error:
            messagebox.showerror("Error", f"Error converting file:\n{error}")
        finally:
            messagebox.showinfo("4dp Conversion Success", f"Successfully converted {file_path} to {file_path.replace('.4dp', '.6dp')}")
