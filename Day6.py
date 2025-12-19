from time import perf_counter

def time_function(func):
    """
    Decorator function to measure runtime of given function.

    Parameters
    ----------
    func : func
        Function to time.

    """
    def wrapper(*args, **kwargs):
        t1 = perf_counter()
        out = func(*args, **kwargs)
        t2 = perf_counter() - t1
        print(f'\n{func.__name__} ran in {t2:.7f} seconds')
        return out
    return wrapper

def get_input(input_file: str='Inputs/Day6_Inputs.txt', cephalopod_math=False) -> list:
    # Extract problems from input file
    if not cephalopod_math:
        with open(input_file) as f:
            lines = [l.strip().split() for l in f.readlines()]

        # If extracting normally, split columns into numbers and operation to form each problem
        problems = [[lines[-1][i], tuple(int(l[i]) for l in lines[:-1])] for i in range(len(lines[0]))]

        return problems

    # If extracting using cephalopod math format, only strip newlines from input
    with open(input_file) as f:
        lines = [l.strip('\n') for l in f.readlines()]

    # Loop through columns, from right-to-left
    i = len(lines[0]) - 1
    problems = []
    while i >= 0:
        numbers = []
        operation = None
        # Until empty column is reached, extract new column of numbers
        while i >= 0 and any(new_num := [lines[r][i].strip() for r in range(len(lines))]):
            # Build number from column
            numbers.append(int(''.join(new_num[:-1])))
            # Extract operation if present
            if new_num[-1]:
                operation = new_num[-1]
            i -= 1
        # Add new problem to list
        problems.append([operation, tuple(numbers)])
        i -= 1

    return problems

import operator
from functools import reduce

@time_function
def Day6_Part1(input_file: str='Inputs/Day6_Inputs.txt') -> int:
    # Parse input file and extract problems
    problems = get_input(input_file)
    grand_total = 0
    for problem in problems:
        # For each problem, find sum or product of numbers as required
        if problem[0] == '+':
            grand_total += sum(n for n in problem[1])
        elif problem[0] == '*':
            grand_total += reduce(operator.mul, problem[1])
        else:
            raise Exception(f"Unrecognised operation {problem[0]}")
    
    return grand_total

@time_function
def Day6_Part2(input_file: str='Inputs/Day6_Inputs.txt') -> int:
    # Parse input file and extract problems usign cephalopod math format
    problems = get_input(input_file, cephalopod_math=True)
    grand_total = 0
    for problem in problems:
        # For each problem, find sum or product of numbers as required
        if problem[0] == '+':
            grand_total += sum(n for n in problem[1])
        elif problem[0] == '*':
            grand_total += reduce(operator.mul, problem[1])
        else:
            raise Exception(f"Unrecognised operation {problem[0]}")
    
    return grand_total
