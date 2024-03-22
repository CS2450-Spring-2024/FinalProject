"""
In this file, there are constants defined for all our opcodes. This way, we can
more easily write programs, like this:
```
program = [
    WRITE + 1, # Because WRITE = 11 * 100, this puts 1101 in $0
    123, # This puts 123 in $1
    HALT
]
CPU(program)
CPU.run_until_halt()
```

When this program is run, it will print 123, then halt.
"""

READ = 10 * 100
WRITE = 11 * 100
LOAD = 20 * 100
STORE = 21 * 100
ADD = 30 * 100
SUBTRACT = 31 * 100
DIVIDE = 32 * 100
MULTIPLY = 33 * 100
BRANCH = 40 * 100
BRANCHNEG = 41 * 100
BRANCHZERO = 42 * 100
HALT = 43 * 100


import tkinter as tk

from uvsim.constants import FONT

class Opcodes:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.opcodes = [
            ("READ", 10 * 100, "Read a word from the keyboard into a specific location in memory."),
            ("WRITE", 11 * 100, "Write a word from a specific location in memory to screen."),
            ("LOAD", 20 * 100, "Load a word from a specific location in memory into the accumulator."),
            ("STORE", 21 * 100, "Store a word from the accumulator into a specific location in memory."),
            ("ADD", 30 * 100, "Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)."),
            ("SUBTRACT", 31 * 100, "Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)."),
            ("DIVIDE", 32 * 100, "Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator)."),
            ("MULTIPLY", 33 * 100, "multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)."),
            ("BRANCH", 40 * 100, "Branch to a specific location in memory."),
            ("BRANCHNEG", 41 * 100, "Branch to a specific location in memory if the accumulator is negative."),
            ("BRANCHZERO", 42 * 100, "Branch to a specific location in memory if the accumulator is zero."),
            ("HALT", 43 * 100, "Pause the program."),
        ]

        self.master.geometry("600x400")
        self.master.title("Tutorial")
        self.master.configure()

        # self.master_frame = tk.Frame(self.master)

        self.labels = []
        for i, (name, opcode, desc) in enumerate(self.opcodes):
            ele = tk.Label(self.master, text=name)
            ele.grid(row=i, column=0, sticky="se", padx=50, pady=20)

        # self.master_frame.pack(fill="both", expand=True)
