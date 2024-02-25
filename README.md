# UVSim
UVSim is a simulator for a simple computer. It has a memory size of 100 words, and operates on signed integers.

# Requirements
- Windows/Linux/MacOS (Others are untested)
- Python 3.10+
- Pillow Python library

# Installation
1. `git clone https://github.com/CS2450-Spring-2024/FinalProject.git`
2. `cd FinalProject`
3. `python3 -m pip install pillow`
5. `python3 -m pip install pytest` (Optional)

# Note on running the GUI
The following video explains the process of running the GUI
[![IMAGE ALT TEXT](http://img.youtube.com/vi/ivGIeuorvso/0.jpg)](http://www.youtube.com/watch?v=ivGIeuorvso "Running in GUI mode")

# Running UVSim
### Running in GUI mode
Run `python3 -m uvsim` in the root directory of the project.

### Running in CLI line by line mode
Run `python3 -m uvsim --cli` in the root directory of the project.

### Running in CLI file mode
Run `python3 -m uvsim --file FILE` in the root directory of the project.

### Showing opcode information
Run `python3 -m uvsim --opcode [OPCODE]` in the root directory of the project.

For more information, run `python3 -m uvsim --help`

# Programming
Programs are written in [BasicML](#basicml-instructions). Programs can be read from a file, or line by line as they are entered in the CLI.
The basic format for instruction words are 2 base 10 digits for the opcode, followed by two base 10 digits for the data. For example, to `LOAD` (opcode 20) the contents of memory address `12` into the accumulator, the instruction word would be `2012`. All programs should contain a `HALT` instruction, but this is not necessary if the program runs to the end of memory.
Every BasicML program should be terminated with the word `-99999`.
If the simulator tries to execute a word that is not an opcode, the simulation ends.
Each word should be preceded by either + or -. However, this is not enforced. In any case, the simulator interprets words with no preceding sign character as positive.
Program files are plain text files.
Program files should have 1 trailing newline.

For example programs, see the example_programs directory in the root of the repository.

## BasicML Instructions

| Type    | Name       | Op | Description                                                                                                                |
|---------|------------|----|----------------------------------------------------------------------------------------------------------------------------|
| I/O     | READ       | 10 | Read a word from the keyboard into a specific location in memory.                                                          |
| I/O     | WRITE      | 11 | Write a word from a specific location in memory to screen.                                                                 |
| I/O     | LOAD       | 20 | Load a word from a specific location in memory into the accumulator.                                                       |
| I/O     | STORE      | 21 | Store a word from the accumulator into a specific location in memory.                                                      |
| Math    | ADD        | 30 | Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).        |
| Math    | SUBTRACT   | 31 | Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator). |
| Math    | DIVIDE     | 32 | Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).     |
| Math    | MULTIPLY   | 33 | multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).   |
| Control | BRANCH     | 40 | Branch to a specific location in memory.                                                                                   |
| Control | BRANCHNEG  | 41 | Branch to a specific location in memory if the accumulator is negative.                                                    |
| Control | BRANCHZERO | 42 | Branch to a specific location in memory if the accumulator is zero.                                                        |
| Control | HALT       | 43 | Pause the program.                                                                                                         |

# Testing

To run the project tests, run `pytest` in the command line in the root directory of the project.
