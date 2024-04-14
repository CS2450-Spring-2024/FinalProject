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

from uvsim.constants import WORD_SIZE


READ = 10 * WORD_SIZE
WRITE = 11 * WORD_SIZE
LOAD = 20 * WORD_SIZE
STORE = 21 * WORD_SIZE
ADD = 30 * WORD_SIZE
SUBTRACT = 31 * WORD_SIZE
DIVIDE = 32 * WORD_SIZE
MULTIPLY = 33 * WORD_SIZE
BRANCH = 40 * WORD_SIZE
BRANCHNEG = 41 * WORD_SIZE
BRANCHZERO = 42 * WORD_SIZE
HALT = 43 * WORD_SIZE

OPCODES = [
    READ,
    WRITE,
    LOAD,
    STORE,
    ADD,
    SUBTRACT,
    DIVIDE,
    MULTIPLY,
    BRANCH,
    BRANCHNEG,
    BRANCHZERO,
    HALT
]
