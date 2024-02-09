from main import get_program_from_file, validate_program
import constants
from opcodes import *

def test_parsing_test_programs():
    validate_program(get_program_from_file("test_programs/Test1.txt"))
    validate_program(get_program_from_file("test_programs/Test2.txt"))

def test_max_length():
    program = [BRANCH + i + 1 for i in range(constants.MEM_SIZE + 10)]
    program.append(constants.TERMINAL_WORD)
    try:
        validate_program(program)
    except AssertionError:
        pass
    else:
        assert False, "No error was given when we tried to parse a program with length > cpu.MEM_SIZE!"

def test_no_terminal_word():
    program = [BRANCH + i + 1 for i in range(constants.MEM_SIZE - 10)]
    try:
        validate_program(program)
    except AssertionError:
        pass
    else:
        assert False, "No error was given when we tried to parse a program with no terminal word!"
