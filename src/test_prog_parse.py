import pytest
from main import get_program_from_file, validate_program
import constants
from opcodes import *

def test_parsing_test_programs():
    validate_program(get_program_from_file("test_programs/Test1.txt"))
    validate_program(get_program_from_file("test_programs/Test2.txt"))

def test_max_length():
    program = [BRANCH + i + 1 for i in range(constants.MEM_SIZE + 10)]
    program.append(constants.TERMINAL_WORD)

    with pytest.raises(AssertionError) as e_info:
        validate_program(program)

def test_no_terminal_word():
    program = [BRANCH + i + 1 for i in range(constants.MEM_SIZE - 10)]
    with pytest.raises(AssertionError) as e_info:
        validate_program(program)
