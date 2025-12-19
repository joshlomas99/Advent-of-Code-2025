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

def get_input(input_file: str='Inputs/Day5_Inputs.txt') -> list:
    # Extract lines from input file
    with open(input_file) as f:
        lines = [l.strip() for l in f.readlines()]
    
    i = 0
    # Extract and split ranges of fresh IDs before first empty line
    fresh_ranges = []
    while lines[i]:
        fresh_ranges.append(tuple(int(n) for n in lines[i].split('-')))
        i += 1
    
    i += 1
    # Extract list of ingredient IDs
    ingredients = set()
    while i < len(lines):
        ingredients.add(int(lines[i]))
        i += 1
    
    return fresh_ranges, ingredients

@time_function
def Day5_Part1(input_file: str='Inputs/Day5_Inputs.txt') -> int:
    # Parse input file and extract fresh ID ranges and ingredient IDs
    num_fresh = 0
    fresh_ranges, ingredients = get_input(input_file)
    # Loop through ingredient IDs
    for i in ingredients:
        # Check through fresh ID ranges
        for l, h in fresh_ranges:
            # If any matching ranges are found:
            if l <= i and i <= h:
                # Add one to count of fresh ingredients and move to next ingredient
                num_fresh += 1
                break
    
    return num_fresh

@time_function
def Day5_Part2(input_file: str='Inputs/Day5_Inputs.txt') -> int:
    # Parse input file and extract fresh ID ranges and ingredient IDs
    fresh_ranges, _ = get_input(input_file)
    # Sort ranges by starting value
    fresh_ranges = sorted(fresh_ranges, key=lambda x: x[0])
    # Create new list with overlapping ranges combined together, start with lowest range
    combined_ranges = [list(fresh_ranges[0])]
    # Loop through all remaining ranges
    for low, high in fresh_ranges[1:]:
        # If next range starts within last one in combined list, extend this range
        if low <= combined_ranges[-1][1]:
            combined_ranges[-1][1] = max(combined_ranges[-1][1], high)
        # Else add a new range
        else:
            combined_ranges.append([low, high])

    # Sum total inclusive lengths of combined ranges
    num_all_fresh = sum(h - l + 1 for l, h in combined_ranges)
    
    return num_all_fresh
