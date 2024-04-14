from uvsim.opcodes import *
from uvsim.parse import parse_word
from uvsim.constants import WORD_SIZE, MEM_SIZE

OK = 0
ERROR_ILLEGAL_INSTRUCTION = 1
ERROR_INVALID_INPUT = 2
ERROR_DIVIDE_BY_ZERO = 3


def line_to_op_data(line):
    """
    Purpose:
        pulls opcode and data from an instruction line.
    Input Parameters:
        line: An instruction line from memory.
    Return Value:
        A tuple that holds the opcode and data.
    Pre-conditions:
        A valid instruction line must be passed in.
    Post-conditions:
        The opcode and data are extracted from the instruction line and returned.
    """
    data = line % WORD_SIZE
    opcode = (line - data)
    return (opcode, data)

def error_code_to_text(code, program_counter):
    """
    Purpose:
        Converts error codes into human readable error messages.
    Input Parameters:
        code: An error code.
    Return Value:
        A string with the correct error message.     
    Pre-conditions: 
        An erroneous code must be passed in.      
    Post-conditions:
        The error code is converted to a human-readable string and returned. 
    """
    error_codes = {
        OK: "",
        ERROR_ILLEGAL_INSTRUCTION: f"Illegal opcode at ${program_counter}",
        ERROR_INVALID_INPUT: "Invalid input",
        ERROR_DIVIDE_BY_ZERO: f"Tried to divide by zero at ${program_counter}",
    }

    return error_codes[code]

class CPU:
    """
    CPU Class
    Purpose of the Class
    The CPU class represents a Central Processing Unit that does instructions stored in memory.
    It interacts with memory and does various operations based on the opcode of the current instruction.

    Class Attributes:
        self.accumulator : An integer that stored the data we are working with.
        self.program_counter : An Integer that counts the steps in the program
        self.memory : An array that represents the memory of the CPU
        self.halted : A boolean value that represents the state of the program
    """
    OK = OK
    ERROR_ILLEGAL_INSTRUCTION = ERROR_ILLEGAL_INSTRUCTION
    ERROR_INVALID_INPUT = ERROR_INVALID_INPUT
    ERROR_DIVIDE_BY_ZERO = ERROR_DIVIDE_BY_ZERO

    def __init__(self, memory):
        self.accumulator = 0
        self.program_counter = 0
        self.memory = memory
        self.halted = True

    def run_until_halt(self):
        """
        Purpose:
            Does instructions in a loop until the CPU is halted.
        Input Parameters:
            None.
        Return Value:
            An error code with the reason for halting.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
        Post-conditions:
            The CPU could be halted, and the state of the memory may be modified.
        """
        self.halted = False
        while True:
            if self.program_counter > MEM_SIZE - 1:
                self.halted = True
            if self.halted:
                return OK

            result = self.run_one_instruction()
            assert result is not None, "All instructions should return an error code"
            if result != OK:
                self.halted = True
                return result

    def run_one_instruction(self):
        """
        Purpose:
            Does a single instruction.
        Input Parameters:
            None.
        Return Value:
            An error code saying the result of the instruction that was executed.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
        Post-conditions:
            The state of the memory and CPU registers may be modified.
        """
        line = self.memory[self.program_counter]
        opcode, data = line_to_op_data(line)

        # Apologies if this section is convoluted, I could have used a bunch of if-else, but I think this is cleaner.
        # All this section does is match the opcode from memory to the function that needs to be run.
        # If the opcode doesn't match any of our defined operations, we call panic().
        return {
            READ: lambda: self.read(data),
            WRITE: lambda: self.write(data),
            LOAD: lambda: self.load(data),
            STORE: lambda: self.store(data),
            ADD: lambda: self.add(data),
            SUBTRACT: lambda: self.subtract(data),
            DIVIDE: lambda: self.divide(data),
            MULTIPLY: lambda: self.multiply(data),
            BRANCH: lambda: self.branch(data),
            BRANCHNEG: lambda: self.branchneg(data),
            BRANCHZERO: lambda: self.branchzero(data),
            HALT: lambda: self.halt(data),
        }.get(opcode, lambda: ERROR_ILLEGAL_INSTRUCTION)()

    def read(self, data, user_input=False): # Tanner
        """
        Purpose:
            Reads input from the user and stores it in memory.
        Input Parameters:
            data: The memory location where the input will be stored.
            user_input: User-provided input.
        Return Value:
            An error code showing the result of the operation.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
        Post-conditions:
            The memory location is updated with the user input.
        """
        if not user_input: # if user_input is not set, get input from cli.
            user_input = input("Enter a word: ")
        try:
            self.memory[data] = parse_word(user_input, self.program_counter)

        except ValueError:
            return ERROR_INVALID_INPUT

        self.program_counter += 1
        return OK

    def write(self, data): # Tanner
        """
        Purpose:
            Writes a word from memory to the console.
        Input Parameters:
            data: The memory location of the word that will be written.
        Return Value:
            An error code showing the result of the operation.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
        Post-conditions:
            The word is printed to the console.
        """
        word_to_write = self.memory[data]
        print(f"Word from memory: {word_to_write}" )

        self.program_counter += 1

        return OK

    def load(self, data):  # Tanner
        """
        Purpose:
            Loads a word from memory into the accumulator.
        Input Parameters:
            data: The memory location of the word that will be loaded.
        Return Value:
            An error code showing the result of the operation.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
        Post-conditions:
            The accumulator is updated with the loaded word.
        """
        self.accumulator = self.memory[data]
        self.program_counter += 1
        return OK

    def store(self, data):
        """
        Purpose:
            Stores the value of the accumulator into a memory location.
        Input Parameters:
            data: The memory location where the accumulator value will be stored.
        Return Value:
            An error code showing the result of the operation.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
        Post-conditions:
            The specified memory location is updated with the accumulator value.
        """
        # Store the value of the accumulator into the  memory location.
        self.memory[data] = self.accumulator  # Frank
        self.program_counter += 1
        return OK

    def add(self, data):  # Frank
        """
        Purpose:
            Adds the value at a specified memory location to the accumulator.
        Input Parameters:
            data: The memory location of the value that will be added.
        Return Value:
            An error code showing the result of the operation.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
        Post-conditions:
            The accumulator is updated with the addition result.
        """
        # Add the value at the memory location to the accumulator.
        self.accumulator += self.memory[data]
        self.program_counter += 1
        return OK

    def subtract(self, data):
        """
        Purpose:
            Subtracts the value at a specified memory location from the accumulator.
        Input Parameters:
            data: The memory location of the value that will be subtracted.
        Return Value:
            An error code showing the result of the operation.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
        Post-conditions:
            The accumulator is updated with the subtraction result.
        """
        # Subtract the value at the specified memory location from the accumulator.
        self.accumulator -= self.memory[data]  # Frank
        self.program_counter += 1
        return OK

    def divide(self, data):  # Kevin
        """
        Purpose:
            Divides the accumulator by the value at a specified memory location.
        Input Parameters:
            data: The memory location of the number that will be divided.
        Return Value:
            An error code showing the result of the operation.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
            The divisor can't be zero.
        Post-conditions:
            The accumulator is updated with the division result.
        """
        if self.memory[data] == 0:
            return ERROR_DIVIDE_BY_ZERO
        self.accumulator /= self.memory[data]
        self.program_counter += 1
        return OK

    def multiply(self, data):  # Kevin
        """
        Purpose:
            Multiplies the accumulator by the value at a specified memory location.
        Input Parameters:
            data: The memory location of the number that will multiply.
        Return Value:
            An error code showing the result of the operation.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
        Post-conditions:
            The accumulator is updated with the multiplication result.
        """
        self.accumulator *= self.memory[data]
        self.program_counter += 1
        return OK

    def branch(self, data):  # Kevin
        """
        Purpose:
            Branches to a specified memory location unconditionally.
        Input Parameters:
            data: The memory location to branch to.
        Return Value:
            An error code showing the result of the operation.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
        Post-conditions:
        The program counter is updated with the branch address.
        """
        self.program_counter = data
        return OK

    def branchneg(self, data):  # Noah
        """
        Purpose:
            Branches to a specified memory location if the accumulator is negative.
        Input Parameters:
            data: The memory location to branch to if the accumulator is negative.
        Return Value:
            An error code showing the result of the operation.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
        Post-conditions:
            The program counter may be updated based on the accumulator value.
        """
        if self.accumulator < 0:
            self.program_counter = data
        else:
            self.program_counter += 1
        return OK

    def branchzero(self, data):  # Noah
        """
        Purpose:
            Branches to a specified memory location if the accumulator is zero.
        Input Parameters:
            data: The memory location to branch to if the accumulator is zero.
        Return Value:
            An error code showing the result of the operation.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
        Post-conditions:
            The program counter may be updated based on the accumulator value.
        """
        if self.accumulator == 0:
            self.program_counter = data
        else:
            self.program_counter += 1
        return OK

    def halt(self, data):  # Noah
        """
        Purpose:
            Halts the CPU.
        Input Parameters:
            data:
        Return Value:
            An error code showing the result of the operation.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
        Post-conditions:
            The CPU is halted.
        """
        self.halted = True
        self.program_counter += 1
        return OK

    def reset(self):
        """
        Purpose:
            Resets the CPU to its initial state.
        Input Parameters:
            None.
        Return Value:
            None.
        Pre-conditions:
            None.
        Post-conditions:
            The CPU is reset to its initial state.
        """
        for i in range(WORD_SIZE):
            self.memory[i] = 0
        self.halted = True
        self.program_counter = 0
        self.accumulator = 0

    def resume(self):
        """
        Purpose:
            Resumes execution of the CPU until it is halted.
        Input Parameters:
            None.
        Return Value:
            None.
        Pre-conditions:
            The CPU needs to be initialized with a valid memory array.
        Post-conditions:
            The CPU may be halted, and the state of the memory may be modified.
        """
        self.halted = False
        self.run_until_halt()
