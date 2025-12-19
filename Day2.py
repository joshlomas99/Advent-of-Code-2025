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

import numpy as np

def get_input(input_file: str='Inputs/Day2_Inputs.txt', strings=False) -> list:
    # Extract lines from input file
    with open(input_file) as f:
        # Extract and split range bounds
        if strings:
            id_ranges = [tuple(i for i in r.split('-')) for r in f.readlines()[0].strip().split(',')]
        else:
            id_ranges = [tuple(int(i) for i in r.split('-')) for r in f.readlines()[0].strip().split(',')]

    return id_ranges

@time_function
def Day2_Part1(input_file: str='Inputs/Day2_Inputs.txt') -> int:
    # Parse input file and extract range bounds
    id_ranges = get_input(input_file)
    # Sum invalid IDs
    invalid_sum = 0
    for id_range in id_ranges:
        # Loop through range
        for i in range(id_range[0], id_range[1]+1):
            # Count number of digits in ID
            id_len = (int(np.log10(i)))+1
            # If not even length, skip
            if id_len%2:
                continue
            # Divide number in two and add to sum if the parts are equal
            power = int(id_len/2)
            if i%(10**power) == i//(10**power):
                invalid_sum += i
    
    return invalid_sum

def is_invalid(i):
    # Count number of digits in ID
    id_len = (int(np.log10(i)))+1
    # Loop through possible lengths of repeating segment
    for power in range(1, id_len):
        # Skip lengths which don't divide correctly
        if id_len%power:
            continue
        # Track parts of number
        parts = dict()
        i_div, i_rem = i, 0
        # Split number into parts of length "power"
        while i_div > 0 and (int(np.log10(i_div)))+1 >= power:
            i_div, i_rem = i_div//(10**power), i_div%(10**power)
            if i_rem in parts:
                parts[i_rem] += 1
            else:
                parts[i_rem] = 1
        # If there's only one part, appearing multiple times, it is repeating and the ID is invalid
        if len(parts) == 1 and parts[i_rem] > 1:
            return True

    return False

from tqdm import tqdm

@time_function
def Day2_Part2(input_file: str='Inputs/Day2_Inputs.txt') -> int:
    # Parse input file and extract range bounds
    id_ranges = get_input(input_file)
    # Sum invalid IDs
    invalid_sum = 0
    for id_range in tqdm(id_ranges):
        # Loop through range
        for i in range(id_range[0], id_range[1]+1):
            # If invalid, add to sum
            if is_invalid(i):
                invalid_sum += i
    
    return invalid_sum

def sum_invalid_fast(id_range, fix_num_rep=None):
    # Alternate approach where all possible invalid IDs in a range are constructed, rather than
    # looping through every ID and checking for invalidity
    invalid_sum = 0
    # If range crosses over a power of 10 (different numbers of digits in low and high bounds),
    # split into seperate ranges each covering only a single ID length
    low_id_len = len(id_range[0])
    high_id_len = len(id_range[1])
    if low_id_len != high_id_len:
        id_range_split = [(id_range[0], str((10**low_id_len)-1))]
        id_len = low_id_len
        while id_len < high_id_len - 1:
            id_range_split.append((str(10**id_len), str((10**(id_len+1))-1)))
            id_len += 1
        id_range_split.append((str(10**(high_id_len-1)), id_range[1]))
    else:
        id_range_split = [id_range]
    # Loop over split ID ranges
    for r in id_range_split:
        # Track IDs with set to remove duplicates
        invalid_ids = set()
        id_len = len(r[0])
        # Option to fix number of repeated segments (for part 1)
        if not fix_num_rep:
            # Or just try every possibility
            rep_lens = range(1, id_len)
        else:
            if id_len%fix_num_rep:
                continue
            rep_lens = [int(id_len/fix_num_rep)]
        for rep_len in rep_lens:
            # Skip segment lengths which don't divide into the ID length
            if id_len%rep_len:
                continue
            # Extract digits corresponding to first repeated segment of the given length
            rep_digits = (r[0][:rep_len], r[1][:rep_len])
            # Loop through and construct all possible invalid IDs in the range by repeating the
            # segment until the ID is the correct length
            for rep_test in range(int(rep_digits[0]), int(rep_digits[1])+1):
                test_id = int(str(rep_test)*int(id_len/rep_len))
                # If this ID falls within the given range, add to set
                if test_id >= int(r[0]) and test_id <= int(r[1]):
                    invalid_ids.add(test_id)
        # Add sum of unique invalid IDs in given range
        invalid_sum += sum(invalid_ids)

    return invalid_sum

@time_function
def Day2_Part1_Fast(input_file: str='Inputs/Day2_Inputs.txt') -> int:
    # Parse input file and extract range bounds
    id_ranges = get_input(input_file, strings=True)
    # Sum invalid IDs
    invalid_sum = 0
    for id_range in id_ranges:
        # Add sum of invalid IDs from range, fix to 2 segments
        invalid_sum += sum_invalid_fast(id_range, fix_num_rep=2)

    return invalid_sum


@time_function
def Day2_Part2_Fast(input_file: str='Inputs/Day2_Inputs.txt') -> int:
    # Parse input file and extract range bounds
    id_ranges = get_input(input_file, strings=True)
    # Sum invalid IDs
    invalid_sum = 0
    for id_range in id_ranges:
        # Add sum of invalid IDs from range
        invalid_sum += sum_invalid_fast(id_range)

    return invalid_sum
    
