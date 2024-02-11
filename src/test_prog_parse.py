import pytest
from main import get_program_from_file
import constants
from opcodes import *
from parse import parse_str, parse_word, validate_program

def test_parsing_test_programs():
    get_program_from_file("example_programs/Test1.txt")
    get_program_from_file("example_programs/Test2.txt")

def test_max_length():
    program = [BRANCH + i + 1 for i in range(constants.MEM_SIZE + 10)]
    program.append(constants.TERMINAL_WORD)

    with pytest.raises(AssertionError) as e_info:
        program = validate_program(program)

def test_no_terminal_word():
    program = [BRANCH + i + 1 for i in range(constants.MEM_SIZE - 10)]
    with pytest.raises(AssertionError) as e_info:
        program = validate_program(program)

def test_parse_all_opcodes():
    cases = [
        ("""+1000\n+1100\n+2000\n+2100\n+3000\n+3100\n+3200\n+3300\n+4000\n+4100\n+4200\n+4300\n-99999""", [READ, WRITE, LOAD, STORE, ADD, SUBTRACT, DIVIDE, MULTIPLY, BRANCH, BRANCHNEG, BRANCHZERO, HALT, constants.TERMINAL_WORD])
    ]

    for arg, expected in cases:
        expected = validate_program(expected)
        program = parse_str(arg)
        assert expected == program
