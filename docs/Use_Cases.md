# Documentation

This is the documentation file.
## Introduction
UVSim is a virtual machine simulator designed for computer Engineering students to learn machine language and computer architecture. By simulating a simple but powerful environment, UVSim allows students to write, load, and execute BasicML (Basic Machine Language) programs. This document outlines the high-level functionality, user stories, and detailed use cases for UVSim.

## User Stories
### Story 1: As a Computer Engineering Student
A computer Engineering student, wants to be able to write BasicML programs and execute them on UVSim so that they can learn about machine language and computer architecture. This includes inputting data, performing arithmetic operations, and controlling the flow of the program.

### Story 2: As an Instructor
As an instructor, they want to provide a tool like UVSim to their students so they can practice and understand the concepts of machine language and computer architecture in a controlled environment. This tool should help them understand how instructions are executed by the CPU, how data is managed in memory, and how arithmetic and control operations affect program execution.

## Use Cases
### Use Case 1: Load a Program
Actor: Student

Description: Load a BasicML program into UVSim's memory starting at location 00.
Steps:
1) The student writes or opens a BasicML program.
2) The student loads the program into UVSim's memory.
3) UVSim validates the program and allocates it starting from memory location 00.

### Use Case 2: Write Data to Memory
Actor: Student

Description: Use the READ instruction to input a word from the keyboard into a specific location in memory.
Steps:
1) The student inputs a READ instruction into their program.
2) UVSim prompts the student to input a word when the READ instruction is executed.
3) The student inputs the word, and UVSim stores it in the specified memory location.

### Use Case 3: Display Data from Memory
Actor: Student

Description: Use the WRITE instruction to display a word from a specific memory location on the screen.
Steps:
1) The student inputs a WRITE instruction into their program.
2) When executed, UVSim reads the word from the specified memory location.
3) UVSim displays the word on the screen.

### Use Case 4: Load a Word into the Accumulator
Actor: Student

Description: Use the LOAD instruction to load a word from memory into the accumulator.
Steps:
1) The student inputs a LOAD instruction into their program.
2) UVSim loads the word from the specified memory location into the accumulator.

### Use Case 5: Store the Accumulator's Value in Memory
Actor: Student

Description: Use the STORE instruction to store the word from the accumulator into a specific memory location.
Steps:
1) The student inputs a STORE instruction into their program.
2) UVSim stores the word from the accumulator into the specified memory location.

### Use Case 6: Perform Arithmetic Operations
Actor: Student

Description: Use ADD, SUBTRACT, DIVIDE, and MULTIPLY instructions to perform arithmetic operations with the accumulator and memory.
Steps:
1) The student inputs an arithmetic instruction into their program.
2) UVSim performs the specified operation between the accumulator's word and the word from the specified memory location, storing the result in the accumulator.

### Use Case 7: Branch Execution
Actor: Student

Description: Use BRANCH, BRANCHNEG, and BRANCHZERO instructions to control the flow of the program based on the accumulator's state.
Steps:
1) The student inputs a branching instruction into their program.
2) Depending on the accumulator's state and the instruction, UVSim alters the execution flow to the specified memory location.

### Use Case 8: Halt the Program
Actor: Student

Description: Use the HALT instruction to pause the program's execution.
Steps:
1) The student inputs a HALT instruction into their program.
2) UVSim stops executing the program when the HALT instruction is encountered.

### Use Case 9: Error Handling
Actor: UVSim

Description: Handle errors gracefully, such as invalid instructions or arithmetic errors.
Steps:
1) During execution, UVSim encounters an error.
2) UVSim displays an error message indicating the type of error and the location.
3) Execution is halted or the student is prompted to correct the error, depending on the situation.

### Use Case 10: Program Reset and Memory Clear
Actor: Student

Description: Reset the UVSim program and clear all memory locations for a fresh start.
Steps:
1) The student decides to start over with a new program.
2) The student resets UVSim, clearing the memory and accumulator.
3) UVSim is now ready for a new program to be loaded and executed.

## Conclusion
The UVSim design document outlines a comprehensive approach to creating a virtual machine simulator for educational purposes. Through detailed user stories and use cases, it provides a roadmap for developing a tool that will help computer engineering  students grasp the fundamentals of machine language and computer architecture.
