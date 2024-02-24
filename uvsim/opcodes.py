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
