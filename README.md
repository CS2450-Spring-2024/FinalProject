# FinalProject

[Videos](https://uvu.instructure.com/courses/576566/pages/class-videos-week-4?module_item_id=12156032)

# Instructions

| Type    | Name       | Op | Description |
|---------|------------|----|-------------------------------------------------------------------|
| I/O     | READ       | 10 | Read a word from the keyboard into a specific location in memory. |
| I/O     | WRITE      | 11 | Write a word from a specific location in memory to screen. |
| I/O     | LOAD       | 20 | Load a word from a specific location in memory into the accumulator. |
| I/O     | STORE      | 21 | Store a word from the accumulator into a specific location in memory. |
| Math    | ADD        | 30 | Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator) |
| Math    | SUBTRACT   | 31 | Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator) |
| Math    | DIVIDE     | 32 | Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator). |
| Math    | MULTIPLY   | 33 | multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator). |
| Control | BRANCH     | 40 | Branch to a specific location in memory |
| Control | BRANCHNEG  | 41 | Branch to a specific location in memory if the accumulator is negative. |
| Control | BRANCHZERO | 42 | Branch to a specific location in memory if the accumulator is zero. |
| Control | HALT       | 43 | Pause the program |

# Testing

To run a test, run `pytest` in the command line in the root directory of the project.
