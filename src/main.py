# todo: create function read program from text file
# todo: create function to read program from command line

from cpu import CPU


def get_program_from_file():
    pass

def get_program_from_cli():
    pass

def parse_program(program: [str]) -> [int]:
    pass

def run_program(program):
    d = CPU(program)
    d.run_until_halt()

def main():
    pass

if __name__ == "__main__":
    main()
