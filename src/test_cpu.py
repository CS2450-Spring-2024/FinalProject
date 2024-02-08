from cpu import CPU
from opcodes import *

# Feel free to copy this test and modify it to test your function
def test_line_to_op_data():
    test_fn = CPU.line_to_op_data

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
    test_di = CPU([2,3,4])
    #idx : (accumulator,expected)
    test_cases ={
        0:(10,5),
        1:(30,10),
        2:(80,20)
    }

    for args, expected in test_cases.items():
        test_di.accumulator = expected[0]
        test_di.divide(args)
        assert test_di.accumulator == expected[1], f"Expected {expected[0]}, Got{test_di.accumulator}"


def test_branch():
    pass


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
        cpu.current_address = addr
        cpu.branchneg(arg)
        assert cpu.current_address == expected


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
        cpu.current_address = addr
        cpu.branchzero(arg)
        assert cpu.current_address == expected

def test_halt():
    cpu = CPU([
        HALT
    ])
    cpu.run_one_instruction()
    assert cpu.halted