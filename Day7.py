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

def get_input(input_file: str='Inputs/Day7_Inputs.txt') -> list:
    # Extract problems from input file
    with open(input_file) as f:
        lines = [l.strip() for l in f.readlines()]

    # Loop through grid and store start position and positions of splitters
    start, splitters = None, set()
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            if lines[r][c] == 'S':
                start = (r, c)
            if lines[r][c] == '^':
                splitters.add((r, c))
    
    return splitters, start

def draw_grid(splitters, beams, start):
    # Draw grid with start, splitter and beam potitions
    height = max(s[0] for s in splitters)
    width = max(max(b[1] for b in beams), max(s[1] for s in splitters))
    for r in range(height):
        row = ''
        for c in range(width):
            if (r, c) == start:
                row += 'S'
            elif (r, c) in splitters:
                row += '^'
            elif (r, c) in beams:
                row += '|'
            else:
                row += '.'
        print(row)

    return

@time_function
def Day7_Part1(input_file: str='Inputs/Day7_Inputs.txt') -> int:
    # Parse input file and extract splitter and start positions
    splitters, start = get_input(input_file)
    # Check max distance of splitters so we know when to stop
    height = max(s[0] for s in splitters)
    # Initiate set of beam coords
    beams = {start}
    # Track height of beams
    i = start[0]
    # Count splits
    num_splits = 0
    # While we have splitters ahead of us
    while i <= height:
        # Create new set of the leading ends of each beam
        new_beams = set()
        # Loop over current beam ends
        for r, c in beams:
            # If next pos is splitter, split beam and count
            if (r+1, c) in splitters:
                num_splits += 1
                new_beams.update({(r+1, c-1), (r+1, c+1)})
            # Else move down
            else:
                new_beams.add((r+1, c))
        # Update set of beam ends
        beams = new_beams.copy()
        i += 1

    return num_splits

from collections import defaultdict

@time_function
def Day7_Part2(input_file: str='Inputs/Day7_Inputs.txt') -> int:
    # Parse input file and extract problems
    splitters, start = get_input(input_file)
    # Check max distance of splitters so we know when to stop
    height = max(s[0] for s in splitters)
    # Initiate dict of beam coords and number of universes reaching this spot
    beams = {start: 1}
    # Track height of beams
    i = start[0]
    # While we have splitters ahead of us
    while i <= height:
        # Create new dict of the leading ends of each beam (default to 0)
        new_beams = defaultdict(int)
        for (r, c), n in beams.items():
            # If next pos is splitter, split beam and add number of current universes to each
            if (r+1, c) in splitters:
                new_beams[(r+1, c-1)] += n
                new_beams[(r+1, c+1)] += n
            # Else move down with current number of universes
            else:
                new_beams[(r+1, c)] += n
        # Update dict of beam ends
        beams = new_beams.copy()
        i += 1

    # Calculate total number of universes
    return sum(beams.values())
