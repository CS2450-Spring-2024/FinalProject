# todo: create function read program from text file
# todo: create function to read program from command line

from cpu import CPU


def get_program_from_file(path) ->[str]:
    '''Get file strip illegal chars'''
    program = []
    with open(path, 'r') as in_file:
        for itm in in_file.readlines():
            program.append(itm.strip('\n'))
    return program    

def get_program_from_cli() -> [str]:
    '''Iter till max mem or command given'''
    count = 0
    program = []
    while count != 100:
        program.append(input(f"{count} ? "))
        if program[-1] =="-99999": # Terminate if -99999 
            program.pop(-1) #probably could be done cleaner
            return program
        count += 1
    return program

def parse_program(program: [str]) -> [int]:
    pass

def run_program(program):
    d = CPU(program)
    d.run_until_halt()

def main():
    pass

if __name__ == "__main__":
    main()
