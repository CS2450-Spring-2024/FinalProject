from uvsim.opcodes import *
from uvsim.parse import parse_word
from uvsim.constants import MEM_SIZE

OK = 0
ERROR_ILLEGAL_INSTRUCTION = 1
ERROR_INVALID_INPUT = 2
ERROR_DIVIDE_BY_ZERO = 3


class CPU:
    OK = OK
    ERROR_ILLEGAL_INSTRUCTION = ERROR_ILLEGAL_INSTRUCTION
    ERROR_INVALID_INPUT = ERROR_INVALID_INPUT
    ERROR_DIVIDE_BY_ZERO = ERROR_DIVIDE_BY_ZERO

    def __init__(self, memory):
        self.accumulator = 0
        self.program_counter = 0
        self.memory = memory
        self.halted = False

    def error_code_to_text(self, code):
        text = ""
        match code:
            case self.OK:
                text = ""
            case self.ERROR_ILLEGAL_INSTRUCTION:
                text = f"Illegal opcode at ${self.program_counter}"
            case self.ERROR_INVALID_INPUT:
                text = "Invalid input"
            case self.ERROR_DIVIDE_BY_ZERO:
                text = f"Tried to divide by zero at ${self.program_counter}"
        return text

    def line_to_op_data(line):
        data = line % 100
        opcode = line - data
        return (opcode, data)

    def run_until_halt(self):
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
        line = self.memory[self.program_counter]
        opcode, data = CPU.line_to_op_data(line)

        def panic():
            return ERROR_ILLEGAL_INSTRUCTION

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
            HALT: lambda: self.halt(data)
        }.get(opcode, panic)()

    def read(self, data, user_input=False): # Tanner
        if not user_input: # if user_input is not set, get input from cli.
            user_input = input("Enter a word: ")
        try:
            # might need to check to see the length of the word.... cant be over len == 4?
            # how does the + or - fit into the project?
            self.memory[data] = parse_word(user_input, self.program_counter)

        except ValueError:
            # Couldn't parse input
            return ERROR_INVALID_INPUT

        self.program_counter += 1
        return OK

    def write(self, data): # Tanner
        word_to_write = self.memory[data]
        print(f"Word from memory: {word_to_write}" )

        self.program_counter += 1

        # return f"Word from memory: {word_to_write}" ## not sure if this is right. I just did this for testing.
        return OK

    def load(self, data): # Tanner
        self.accumulator = self.memory[data]
        self.program_counter += 1
        return OK

    def store(self, data):
        # Store the value of the accumulator into the  memory location.
        self.memory[data]= self.accumulator # Frank
        self.program_counter += 1
        return OK

    def add(self, data): # Frank
        #Add the value at the memory location to the accumulator.
        self.accumulator += self.memory[data]
        self.program_counter += 1
        return OK

    def subtract(self, data):
        # Subtract the value at the specified memory location from the accumulator.
        self.accumulator -= self.memory[data] # Frank
        self.program_counter += 1
        return OK

    def divide(self, data): # Kevin
        if self.memory[data] == 0:
            # print(f"Halted for attempt to divide by zero at {self.program_counter}!")
            return ERROR_DIVIDE_BY_ZERO
        self.accumulator /= self.memory[data]
        self.program_counter += 1
        return OK

    def multiply(self, data): # Kevin
        self.accumulator *= self.memory[data]
        self.program_counter += 1
        return OK

    def branch(self, data): # Kevin
        self.program_counter = data
        return OK

    def branchneg(self, data): # Noah
        if self.accumulator < 0:
            self.program_counter = data
        else:
            self.program_counter += 1
        return OK

    def branchzero(self, data): # Noah
        if self.accumulator == 0:
            self.program_counter = data
        else:
            self.program_counter += 1
        return OK

    def halt(self, data): # Noah
        self.halted = True
        self.program_counter += 1
        return OK

    def reset(self):
        self.memory = [0] * MEM_SIZE
        self.halted = False
        self.program_counter = 0
        self.accumulator = 0

    def resume(self):
        self.halted = False
        self.run_until_halt()
