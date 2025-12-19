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

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)]

def get_input(input_file: str='Inputs/Day4_Inputs.txt') -> list:
    # Extract coords of paper rolls from input file as set
    with open(input_file) as f:
        rolls = {(r, c) for r, l in enumerate(f.readlines()) for c, p in enumerate(l.strip()) if p == '@'}

    return rolls

def count_adjacent_rolls(rolls, roll):
    adjacent_rolls = 0
    # Check all eight adjacent directions
    for d in DIRS:
        # Count adjacent rolls
        if (roll[0]+d[0], roll[1]+d[1]) in rolls:
            adjacent_rolls += 1

    return adjacent_rolls

def print_rolls(rolls, accessible=[]):
    for r in range(max(r[0] for r in rolls)+1):
        row = ''
        for c in range(max(r[1] for r in rolls)+1):
            if (r, c) in accessible:
                row += 'x'
            elif (r, c) in rolls:
                row += '@'
            else:
                row += '.'
        print(row)

    return

@time_function
def Day4_Part1(input_file: str='Inputs/Day4_Inputs.txt') -> int:
    # Parse input file and extract coords of paper rolls
    rolls = get_input(input_file)
    num_accessible = 0
    accessible = []
    # Loop through rolls
    for r, c in rolls:
        # Check for each roll how many are adjacent, if less than 4, add to total
        if count_adjacent_rolls(rolls, (r, c)) < 4:
            num_accessible += 1
            accessible.append((r, c))

    # print_rolls(rolls, accessible)
    
    return num_accessible

@time_function
def Day4_Part2(input_file: str='Inputs/Day4_Inputs.txt') -> int:
    # Parse input file and extract coords of paper rolls
    rolls = get_input(input_file)
    num_removed, num_accessible = 0, 0
    # While some rolls were removed in the last interation (or we are at the beginning)
    while num_accessible > 0 or num_removed == 0:
        # Reset counters
        num_accessible = 0
        accessible = []
        # Create copy of roll coords set to edit during loop
        rolls_copy = rolls.copy()
        # Loop through map
        for r, c in rolls:
            # Check for each roll how many are adjacent, if less than 4, add to total
            if count_adjacent_rolls(rolls, (r, c)) < 4:
                num_accessible += 1
                accessible.append((r, c))
                # Remove roll in copy of map
                rolls_copy.remove((r, c))
        # Add removed rolls to running total
        num_removed += num_accessible
        # Update list of roll coords with removed rolls
        rolls = rolls_copy.copy()

    # print_rolls(rolls, accessible)
    
    return num_removed
