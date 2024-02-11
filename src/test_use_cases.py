import pytest
from constants import MEM_SIZE, TERMINAL_WORD
from cpu import CPU
from opcodes import *


def test_loading_a_program(monkeypatch, capsys):
    # Actor: Student
    # UVSim instance
    uv_sim = CPU([0]*100)

    # Step 1: The student writes or opens a BasicML program.
    program = [1007, # READ into location 07
               1008, # READ into location 08
               2007, # LOAD from location 07
               3008, # ADD from location 08
               2109, # STORE into location 09
               1109, # WRITE from location 09
               HALT, # HALT
               TERMINAL_WORD] # TERMINAL_WORD

    # Load this program into the CPU's memory
    for i, instruction in enumerate(program):
        uv_sim.memory[i] = instruction

    # Mock the calls to input
    monkeypatch.setattr("builtins.input", lambda _: "10")

    # Run the program only up to the READ instruction
    for _ in range(6):
        uv_sim.run_one_instruction()

    # Use capsys to capture the output
    captured = capsys.readouterr()

    # Test if the correct output was printed
    assert "Word from memory: 20" in captured.out

def test_writing_data_to_memory(monkeypatch):
    # Actor: Student
    # UVSim instance
    uv_sim = CPU([0]*100)

    # Step 1: The student inputs a READ instruction into their program.
    uv_sim.memory[0] = 1008  # Read into location 08

    # Mock the calls to input
    monkeypatch.setattr("builtins.input", lambda _: "50")  # Mock user entering '50'

    # Step 2: UVSim prompts the student to input a word when the READ instruction is executed
    # and subsequent step 3: The student inputs the word, and UVSim stores it in the specified memory location
    uv_sim.run_one_instruction()

    assert uv_sim.memory[8] == 50  # The entered data '50' should be in memory location 8

def test_displaying_data_from_memory(monkeypatch, capsys):
    # Actor: Student
    # UVSim instance
    uv_sim = CPU([0]*100)

    # Step 1: The student inputs a WRITE instruction into their program (in this case, writing the value at location 7).
    program = [1107, # WRITE from location 07
               HALT, # HALT
               TERMINAL_WORD] # TERMINAL_WORD

    # Load this program into the CPU's memory
    for i, instruction in enumerate(program):
        uv_sim.memory[i] = instruction

    # Also, let's manually store a word at memory location 7
    uv_sim.memory[7] = 5678

    # Step 2: When executed, UVSim reads the word from the specified memory location.
    # Step 3: UVSim displays the word on the screen.
    uv_sim.run_one_instruction()  # Execute the WRITE instruction

    # Use capsys to capture the output
    captured = capsys.readouterr()

    # Check if the correct output was printed
    assert "Word from memory: 5678" in captured.out

def test_loading_word_into_accumulator():
    # Actor: Student
    # UVSim instance
    uv_sim = CPU([0]*100)

    # Step 1: The student inputs a LOAD instruction into their program.
    # Let's set a value at some address in memory and then LOAD from that.
    uv_sim.memory[7] = 42  # Set memory[7] = 42
    uv_sim.memory[0] = 2000 + 7  # Insert instruction to LOAD from memory[7]

    # Step 2: UVSim loads the word from the specified memory location into
    # the accumulator
    uv_sim.run_one_instruction()

    # Test that loading worked correctly.
    assert uv_sim.accumulator == 42

def test_accumulator_store_instruction(monkeypatch, capsys):
    # UVSim instance
    uv_sim = CPU([0]*100)

    # Step 1: The student inputs a STORE instruction into their program
    # Let's create a simple program with READ, LOAD and STORE instructions
    program = [1007,  # READ into location 07
               2007,  # LOAD from location 07 to accumulator
               2108,  # STORE accumulator into location 08
               1108,  # WRITE from location 08
               HALT,  # HALT
               TERMINAL_WORD]

    # Load this program into the CPU's memory
    for i, instruction in enumerate(program):
        uv_sim.memory[i] = instruction

    # Mock the calls to input to act as the word that the student inputs
    monkeypatch.setattr("builtins.input", lambda _: "15")

    # Run the program only up to the WRITE instruction
    for _ in range(4):
        uv_sim.run_one_instruction()

    # Use capsys to capture the output
    captured = capsys.readouterr()

    # Test if the correct output was printed
    assert "Word from memory: 15" in captured.out

def test_performing_add_operation(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "10")
    program = [READ + 7, READ + 8, LOAD + 7, ADD + 8, STORE + 9, WRITE + 9, HALT, TERMINAL_WORD]
    cpu = CPU([0]*100)
    for i, instruction in enumerate(program):
        cpu.memory[i] = instruction
    cpu.run_until_halt()
    captured = capsys.readouterr()
    assert "Word from memory: 20" in captured.out

def test_performing_subtract_operation(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "10")
    program = [READ + 7, READ + 8, LOAD + 7, SUBTRACT + 8, STORE + 9, WRITE + 9, HALT, TERMINAL_WORD]
    cpu = CPU([0]*100)
    for i, instruction in enumerate(program):
        cpu.memory[i] = instruction
    cpu.run_until_halt()
    captured = capsys.readouterr()
    assert "Word from memory: 0" in captured.out

def test_performing_multiply_operation(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "10")
    program = [READ + 7, READ + 8, LOAD + 7, MULTIPLY + 8, STORE + 9, WRITE + 9, HALT, TERMINAL_WORD]
    cpu = CPU([0]*100)
    for i, instruction in enumerate(program):
        cpu.memory[i] = instruction
    cpu.run_until_halt()
    captured = capsys.readouterr()
    assert "Word from memory: 100" in captured.out

def test_performing_divide_operation(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "10")
    program = [READ + 7, READ + 8, LOAD + 7, DIVIDE + 8, STORE + 9, WRITE + 9, HALT, TERMINAL_WORD]
    cpu = CPU([0]*100)
    for i, instruction in enumerate(program):
        cpu.memory[i] = instruction
    cpu.run_until_halt()
    captured = capsys.readouterr()
    assert "Word from memory: 1" in captured.out

def test_halting_the_program():
    # Actor: Student
    # UVSim instance
    cpu = CPU([0] * MEM_SIZE)

    # Step 1: The student inputs a HALT instruction into their program.
    program = [2000, # LOAD 0
               3100, # ADD 0
               4300, # STORE 300
               HALT, # HALT
               TERMINAL_WORD] # TERMINAL_WORD

    # Load this program into the CPU's memory
    for i, instruction in enumerate(program):
        cpu.memory[i] = instruction

    # Step 2: UVSim stops executing the program when the HALT instruction is encountered.
    cpu.run_until_halt()

    # Test if UVSim has indeed halted
    assert cpu.halted == True, f"CPU should be halted but it wasn't"

def test_invalid_instruction():
    # Actor: UVSim
    # Instantiate UVSim instance
    uv_sim = CPU([0]*100)

    # Load an invalid instruction into the CPU's memory
    invalid_instruction = 6600
    uv_sim.memory[0] = invalid_instruction

    # Run the program
    uv_sim.run_one_instruction()

    # Assert that the CPU has halted due to the invalid instruction
    assert uv_sim.halted

def test_program_reset_and_memory_clear():
    # Actor: Student
    # Step 1: The student decides to start over with a new program.
    # Step 2: The student resets UVSim, clearing the memory and accumulator.

    # UVSim instance
    cpu = CPU([0]*100)

    cpu.memory[5] = 12
    cpu.accumulator = 5
    cpu.current_address = 10
    cpu.halted = True

    cpu.reset()

    assert all(mem == 0 for mem in cpu.memory)
    assert cpu.accumulator == 0
    assert cpu.current_address == 0
    assert not cpu.halted

    # Step 3: UVSim is now ready for a new program to be loaded and executed.
