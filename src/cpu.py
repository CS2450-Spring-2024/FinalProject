from opcodes import *


class CPU:
    def __init__(self, memory):
        self.accumulator = 0
        self.current_address = 0
        self.memory = memory
        self.halted = False

    def line_to_op_data(line):
        data = line % 100
        opcode = line - data
        return (opcode, data)

    def run_until_halt(self):
        while True:
            if self.halted or self.current_address > 99:
                break
            self.run_one_instruction()

    def run_one_instruction(self):
        line = self.memory[self.current_address]
        opcode, data = CPU.line_to_op_data(line)

        def panic():
            print(f"Illegal opcode {opcode} at ${self.current_address}: {line}")
            exit()

        # Apologies if this section is convoluted, I could have used a bunch of if-else, but I think this is cleaner.
        # All this section does is match the opcode from memory to the function that needs to be run.
        # If the opcode doesn't match any of our defined operations, we call panic().
        {
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

    def read(self, data): # Tanner
        pass

    def write(self, data): # Tanner
        pass

    def load(self, data): # Tanner
        pass

    def store(self, data): # Frank
        pass

    def add(self, data): # Frank
        pass

    def subtract(self, data): # Frank
        pass

    def divide(self, data): # Kevin
        self.accumulator /= self.memory[data]

    def multiply(self, data): # Kevin
        self.accumulator *= self.memory[data]

    def branch(self, data): # Kevin
        self.current_address = data

    def branchneg(self, data): # Noah
        if self.accumulator < 0:
            self.current_address = data
        else:
            self.current_address += 1

    def branchzero(self, data): # Noah
        if self.accumulator == 0:
            self.current_address = data
        else:
            self.current_address += 1

    def halt(self, data): # Noah
        self.halted = True
