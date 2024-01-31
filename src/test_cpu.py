
# Feel free to copy this test and modify it to test your function
def test_line_to_op_data():
    from cpu import CPU
    test_fn = CPU.line_to_op_data

    # key is the argument to the fn, val is the expected output
    test_cases = {
        0000: (0, 0),
        1007: (10, 7),
        1008: (10, 8),
        1009: (10, 9),
        1010: (10, 10),
        1109: (11, 9),
        1110: (11, 10),
        2007: (20, 7),
        2009: (20, 9),
        2109: (21, 9),
        3008: (30, 8),
        3110: (31, 10),
        4107: (41, 7),
        4300: (43, 0),
        9900: (99, 0),  # Testing opcode 99, minimal data
        9999: (99, 99),  # Testing opcode 99 with data 99
        1099: (10, 99),  # Testing data 99, opcode 10
        9901: (99, 1),  # Testing opcode 99 with minimal data
        99: (0, 99),  # Edge case: data is 99, opcode is 0
    }

    for input, expected in test_cases.items():
        assert test_fn(input) == expected, f"Failed on input {input}: expected {expected}, got {test_fn(input)}"
