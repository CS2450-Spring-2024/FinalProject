from cpu import CPU
from constants import MEM_SIZE, TERMINAL_WORD
import argparse
from parse import get_program_from_cli, get_program_from_file


def main():
    parser = argparse.ArgumentParser(description="UVSimulator is a barebones computer simulator. Run a program from a file or by entering it line by line.")
    parser.add_argument("-c", "--cli", help=f"Enter a program from the command line. Programs must be at most {MEM_SIZE} words. (Default)", action="store_true", default=True)
    parser.add_argument("-f", "--file", help=f"Reads a program from a file. Programs must be at most {MEM_SIZE} words.")
    parser.add_argument("-o", "--opcode", nargs='?', const=True, default=False, help="Show opcode documentation. May be in the form \"STORE\", or may be an integer. Use with no value to see all opcodes.")
    args = parser.parse_args()

    if args.opcode:
        help_opcodes(args.opcode)

    elif args.file:
        path = args.file
        program = get_program_from_file(path)
        c = CPU(program)
        c.run_until_halt()

    elif args.cli:
        program = get_program_from_cli()
        c = CPU(program)
        c.run_until_halt()


def help_opcodes(arg):
    if type(arg) == bool:
        print("10: READ")
        print("11: WRITE")
        print("20: LOAD")
        print("21: STORE")
        print("30: ADD")
        print("31: SUBTRACT")
        print("32: DIVIDE")
        print("33: MULTIPLY")
        print("40: BRANCH")
        print("41: BRANCHNEG")
        print("42: BRANCHZERO")
        print("43: HALT")
    else:
        match arg:
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

if __name__ == "__main__":
    main()
