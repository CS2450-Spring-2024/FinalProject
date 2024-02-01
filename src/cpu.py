class CPU:
    def __init__(self, memory):
        self.accumulator = 0
        self.current_address = 0
        self.memory = memory
        self.halted = False

    def line_to_op_data(line):
        data = line % 100
        opcode = line // 100
        return (opcode, data)

    def run_one_instruction(self):
        line = self.memory[self.current_address]
        opcode, data = CPU.line_to_op_data(line)

        def panic():
            print(f"Illegal instruction {opcode} at ${self.current_address}: {line}!")
            exit()

        # Apologies if this section is convoluted, I could have used a bunch of if-else, but I think this is cleaner.
        # All this section does is match an opcode to the function that needs to be run.
        # If the opcode doesn't match any of our defined operations, we call panic().
        {
            10: lambda: self.read(data),
            11: lambda: self.write(data),
            20: lambda: self.load(data),
            21: lambda: self.store(data),
            30: lambda: self.add(data),
            31: lambda: self.subtract(data),
            32: lambda: self.divide(data),
            33: lambda: self.multiply(data),
            40: lambda: self.branch(data),
            41: lambda: self.branchneg(data),
            42: lambda: self.branchzero(data),
            43: lambda: self.halt(data)
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
        pass

    def multiply(self, data): # Kevin
        pass

    def branch(self, data): # Kevin
        pass

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
