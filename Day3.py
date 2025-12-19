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

def get_input(input_file: str='Inputs/Day3_Inputs.txt') -> list:
    # Extract lines from input file
    with open(input_file) as f:
        banks = [l.strip() for l in f.readlines()]

    return banks

def highest_joltage(bank, num_batteries):
    # Track digits of final number
    digits = []
    # Track position in bank of prevous digit
    pos_prev = -1
    # Loop over total digits to extract, starting with the highest power of ten
    for digit_pos in range(num_batteries):
        # Check for maximum digit in bank, starting after previous digit position and limiting
        # position so there is room for all remaining digits to be extracted afterwards
        digit = max(int(b) for b in bank[pos_prev+1:-1*(num_batteries-digit_pos-1) if num_batteries-digit_pos-1 > 0 else None])
        # Update previous digit position
        pos_prev = bank[pos_prev+1:].index(str(digit)) + pos_prev+1
        digits.append(str(digit))

    # Convert digits to number
    return int(''.join(digits))

@time_function
def Day3_Part1(input_file: str='Inputs/Day3_Inputs.txt') -> int:
    # Parse input file and extract banks of batteries
    banks = get_input(input_file)
    total_joltage = 0
    # Loop over and extract highest number possible with 2 digits for each, and sum
    for bank in banks:
        total_joltage += highest_joltage(bank, 2)
    
    return total_joltage

@time_function
def Day3_Part2(input_file: str='Inputs/Day3_Inputs.txt') -> int:
    # Parse input file and extract banks of batteries
    banks = get_input(input_file)
    total_joltage = 0
    # Loop over and extract highest number possible with 12 digits for each, and sum
    for bank in banks:
        total_joltage += highest_joltage(bank, 12)
    
    return total_joltage
