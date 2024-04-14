from uvsim.constants import TERMINAL_WORD
from uvsim.cpu import CPU
from uvsim.opcodes import *
from uvsim.parse import validate_program, word_to_op_data_4dp, word_to_op_data

def test_line_to_op_data():
    test_fn = word_to_op_data

    # key is the argument to the fn, val is the expected output
    test_cases = {
        0000: (0, 0),
        10007: (10000, 7),
        10008: (10000, 8),
        10009: (10000, 9),
        10010: (10000, 10),
        11009: (11000, 9),
        11010: (11000, 10),
        20007: (20000, 7),
        20009: (20000, 9),
        21009: (21000, 9),
        30008: (30000, 8),
        31010: (31000, 10),
        41007: (41000, 7),
        43000: (43000, 0),
        99000: (99000, 0),  # Testing opcode 9900, minimal data
        99099: (99000, 99),  # Testing opcode 9900 with data 99
        10099: (10000, 99),  # Testing data 99, opcode 1000
        99001: (99000, 1),  # Testing opcode 9900 with minimal data
        99: (0, 99),  # Edge case: data is 99, opcode is 0
    }

    for args, expected in test_cases.items():
        assert test_fn(args) == expected, f"Failed on input {args}: expected {expected}, got {test_fn(args)}"

def test_line_to_op_data_4dp():
    test_fn = word_to_op_data_4dp

    # key is the argument to the fn, val is the expected output
    test_cases = {
        0000: (0, 0),
        1007: (1000, 7),
        1008: (1000, 8),
        1009: (1000, 9),
        1010: (1000, 10),
        1109: (1100, 9),
        1110: (1100, 10),
        2007: (2000, 7),
        2009: (2000, 9),
        2109: (2100, 9),
        3008: (3000, 8),
        3110: (3100, 10),
        4107: (4100, 7),
        4300: (4300, 0),
        9900: (9900, 0),  # Testing opcode 9900, minimal data
        9999: (9900, 99),  # Testing opcode 9900 with data 99
        1099: (1000, 99),  # Testing data 99, opcode 1000
        9901: (9900, 1),  # Testing opcode 9900 with minimal data
        99: (0, 99),  # Edge case: data is 99, opcode is 0
    }

    for args, expected in test_cases.items():
        assert test_fn(args) == expected, f"Failed on input {args}: expected {expected}, got {test_fn(args)}"

def test_multiply():
    test_mu = CPU([5,10,20])
    #idx : (accumulator,expected)
    test_cases ={
        0:(2,10),
        1:(3,30),
        2:(4,80)
    }

    for args, expected in test_cases.items():
        test_mu.accumulator = expected[0]
        test_mu.multiply(args)
        assert test_mu.accumulator == expected[1], f"Expected {expected[0]}, Got{test_mu.accumulator}"

def test_divide():
    test_di = CPU([2,3,4,4])
    #idx : (accumulator,expected)
    test_cases ={
        0:(10,5),
        1:(30,10),
        2:(80,20),
        3:(0, 0), # Check zero Division
    }

    for args, expected in test_cases.items():
        test_di.accumulator = expected[0]
        test_di.divide(args)
        assert test_di.accumulator == expected[1], f"Expected {expected[0]}, Got{test_di.accumulator}"

def test_multiply_fail():
    test_mu = CPU([1,-2,10, 30, 4])
    #idx : (accumulator,expected)
    test_cases ={
        0:(-1, 1),
        1:(-2, -4),
        2:(0,10),
        3:(1,300),
        4:(0.25, 8),
    }

    for args, expected in test_cases.items():
        test_mu.accumulator = expected[0]
        test_mu.multiply(args)
        assert test_mu.accumulator != expected[1], f"Expected {expected[0]}, Got{test_mu.accumulator}"



def test_branch():
    tests = [
        # (accumulator, branchneg_arg, current_address, post_expected_current_address)
        (-1, 10, 4, 10),  # accumulator is negative
        (0, 10, 4, 10),  # accumulator is zero
        (1, 10, 4, 10),  # accumulator is positive
        (-1, 0, 4, 0),  # accumulator is negative, branchneg_arg is minimum
        (-1, 99, 4, 99),  # accumulator is negative, branchneg_arg is maximum
        (0, 0, 4, 0),  # accumulator is zero, branchneg_arg is minimum
        (0, 99, 4, 99),  # accumulator is zero, branchneg_arg is maximum
        (-1, 10, 4, 10),  # accumulator is just below 0
        (0, 10, 4, 10),  # accumulator is 0
        (1, 10, 4, 10),  # accumulator is just above 0
        (-1, 50, 4, 50),  # accumulator is negative, large positive step
    ]

    for (accum, arg, addr, expected) in tests:
        cpu = CPU([0] * 100)
        cpu.accumulator = accum
        cpu.program_counter = addr
        cpu.branch(arg)
        assert cpu.program_counter == expected


def test_branchneg():
    tests = [
        # (accumulator, branchneg_arg, current_address, post_expected_current_address)
        (-1, 10, 4, 10),  # accumulator is negative
        (0, 10, 4, 5),  # accumulator is zero
        (1, 10, 4, 5),  # accumulator is positive
        (-1, 0, 4, 0),  # accumulator is negative, branchneg_arg is minimum
        (-1, 99, 4, 99),  # accumulator is negative, branchneg_arg is maximum
        (0, 0, 4, 5),  # accumulator is zero, branchneg_arg is minimum
        (0, 99, 4, 5),  # accumulator is zero, branchneg_arg is maximum
        (-1, 10, 4, 10),  # accumulator is just below 0
        (0, 10, 4, 5),  # accumulator is 0
        (1, 10, 4, 5),  # accumulator is just above 0
        (-1, 50, 4, 50),  # accumulator is negative, large positive step
        (-1, -50, 4, -50),  # accumulator is negative, large negative step
    ]

    for (accum, arg, addr, expected) in tests:
        cpu = CPU([0] * 100)
        cpu.accumulator = accum
        cpu.program_counter = addr
        cpu.branchneg(arg)
        assert cpu.program_counter == expected


def test_branchzero():
    tests = [
        # (accumulator, branchzero_arg, current_address, post_expected_current_address)
        (4, 10, 4, 5),
        (0, 10, 4, 10),
        (0, 0, 4, 0),  # accumulator is 0, branchzero_arg is minimum
        (0, 99, 4, 99),  # accumulator is 0, branchzero_arg is maximum
        (1, 0, 4, 5),  # accumulator is non-zero, branchzero_arg is minimum
        (1, 99, 4, 5),  # accumulator is non-zero, branchzero_arg is maximum
        (-1, 10, 4, 5),  # accumulator is just below 0
        (1, 10, 4, 5),  # accumulator is just above 0
        (0, 50, 4, 50),  # accumulator is 0, large positive step
        (0, -50, 4, -50),  # accumulator is 0, large negative step
    ]

    for (accum, arg, addr, expected) in tests:
        cpu = CPU([0] * 100)
        cpu.accumulator = accum
        cpu.program_counter = addr
        cpu.branchzero(arg)
        assert cpu.program_counter == expected

def test_halt():
    cpu = CPU([
        HALT
    ])
    cpu.run_one_instruction()
    assert cpu.halted



def test_read(): # 10 Read a word from the keyboard into a specific location in memory.
    test_rd = CPU([0] * 100)

    test_cases ={
        0: (+1023),
        1: (+1034),
        2: (-4356),
        55: (+5789),
        99: (+5786)
    }

    for args, expected in test_cases.items():
        test_rd.read(args, expected) #figure out a way to test the function that doesn't change the structure of the original function.
        assert test_rd.memory[args] == expected


def test_write(monkeypatch): # 11 Write a word from a specific location in memory to screen.
    test_wrt = CPU([0] * 100)
    test_cases ={
        0: (+0000),
        1: (+1034),
        2: (-4356),
        55: (+5789),
        99: (+5786)
    }

    for args, expected in test_cases.items():
        monkeypatch.setattr("builtins.input", lambda _:args)
        test_wrt.read(args, expected)
        assert test_wrt.memory[args] == expected


def test_load(monkeypatch): # 20 Load a word from a specific location in memory into the accumulator.
    test_wrt = CPU([0] * 100)

    test_cases ={
        0: (+0000),
        1: (+1034),
        2: (-4356),
        55: (+5789),
        99: (+5786)
    }

    for args, expected in test_cases.items():
        monkeypatch.setattr("builtins.input", lambda _:args)
        test_wrt.read(args, expected)
        test_wrt.load(args)
        assert test_wrt.accumulator == expected

def test_read_write_mem_outside_program_space():
    program = [WRITE + 5, HALT, TERMINAL_WORD]
    program = validate_program(program)
    c = CPU(program)
    c.run_until_halt()
