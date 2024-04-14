import pytest
from uvsim.main import get_program_from_file
import uvsim.constants as constants
from uvsim.opcodes import *
from uvsim.parse import parse_str, parse_word, validate_program

def test_parsing_test_programs():
    get_program_from_file("example_programs/Test1.6dp")
    get_program_from_file("example_programs/Test2.6dp")
    get_program_from_file("example_programs/Test3.6dp")
    get_program_from_file("example_programs/fibo.6dp")

    get_program_from_file("example_programs/Test1.4dp", check_6dp=False)
    get_program_from_file("example_programs/Test2.4dp", check_6dp=False)
    get_program_from_file("example_programs/Test3.4dp", check_6dp=False)
    get_program_from_file("example_programs/fibo.4dp", check_6dp=False)

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
        ("""+10000\n+11000\n+20000\n+21000\n+30000\n+31000\n+32000\n+33000\n+40000\n+41000\n+42000\n+43000\n-99999""", [READ, WRITE, LOAD, STORE, ADD, SUBTRACT, DIVIDE, MULTIPLY, BRANCH, BRANCHNEG, BRANCHZERO, HALT, constants.TERMINAL_WORD])
    ]

    for arg, expected in cases:
        expected = validate_program(expected)
        program = parse_str(arg)
        assert expected == program
