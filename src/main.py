from cpu import CPU, MEM_SIZE
import argparse


def get_program_from_file(path) -> [int]:
    '''Get program from file'''

    with open(path, 'r') as in_file:
        program = [parse_word(itm.strip('\n'), i) for i, itm in enumerate(in_file.readlines())]
    return program

def get_program_from_cli() -> [int]:
    '''Get program from CLI'''

    program = []
    while True:
        word = parse_word(input(f"{len(program)} ? "), len(program))
        program.append(word)

        if word == -99999: # Terminate if -99999
            return program

        if len(program) > MEM_SIZE:
            raise AssertionError("Invalid program, must be terminated with -99999!")

def parse_word(word: str, addr: int) -> int:
    try:
        val = int(word)
    except ValueError as e:
        print(f"Could not parse ${addr}: {word}")
        exit()
    return val

def validate_program(program: [int]):
    assert program[-1] == -99999, f"Invalid program, must be terminated with -99999!\nProgram:{program}"
    assert len(program) <= MEM_SIZE, f"Invalid program, must be 100 lines or less!\nProgram:{program}"

def run_program(program):
    d = CPU(program)
    d.run_until_halt()

def run_program_from_file(path):
    program = get_program_from_file(path)
    print(program)
    validate_program(program)
    run_program(program)

def run_program_from_cli():
    program = get_program_from_cli()
    validate_program(program)
    run_program(program)

def main():
    parser = argparse.ArgumentParser(description="UVSimulator is a barebones computer simulator. Run a program from a file or by entering it line by line.")
    parser.add_argument("-c", "--cli", help="Enter a program from the command line. (Default)", action="store_true", default=True)
    parser.add_argument("-f", "--file", help="Reads a program from a file.")
    parser.add_argument("-o", "--opcode", nargs='?', const=True, default=False, help="Show all available opcodes. May be in the form \"STORE\", or may be an integer. Use with no value to see all options.")
    args = parser.parse_args()

    if args.file:
        path = args.file
        run_program_from_file(path)
    elif args.opcode:
        if type(args.opcode) == bool:
            print("""10: READ
11: WRITE
20: LOAD
21: STORE
30: ADD
31: SUBTRACT
32: DIVIDE
33: MULTIPLY
40: BRANCH
41: BRANCHNEG
42: BRANCHZERO
43: HALT""")
        else:
            match args.opcode:
                case "10" | "READ":
                    print("READ: Opcode 10. Read a word from the keyboard into a specific location in memory.")
                case "11" | "WRITE":
                    print("WRITE: Opcode 11. Write a word from a specific location in memory to screen.")
                case "20" | "LOAD":
                    print("LOAD: Opcode 20. Load a word from a specific location in memory into the accumulator.")
                case "21" | "STORE":
                    print("STORE: Opcode 21. Store a word from the accumulator into a specific location in memory.")
                case "30" | "ADD":
                    print("ADD: Opcode 30. Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).")
                case "31" | "SUBTRACT":
                    print("SUBTRACT: Opcode 31. Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator).")
                case "32" | "DIVIDE":
                    print("DIVIDE: Opcode 32. Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).")
                case "33" | "MULTIPLY":
                    print("MULTIPLY: Opcode 33. multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).")
                case "40" | "BRANCH":
                    print("BRANCH: Opcode 40. Branch to a specific location in memory.")
                case "41" | "BRANCHNEG":
                    print("BRANCHNEG: Opcode 41. Branch to a specific location in memory if the accumulator is negative.")
                case "42" | "BRANCHZERO":
                    print("BRANCHZERO: Opcode 42. Branch to a specific location in memory if the accumulator is zero.")
                case "43" | "HALT":
                    print("HALT: Opcode 43. Pause the program.")
                case _:
                    print("Unrecognized opcode, run -o with no value to see all options.")
    elif args.cli:
        run_program_from_cli()


if __name__ == "__main__":
    main()
