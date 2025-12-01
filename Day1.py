def get_input(input_file: str='Inputs/Day1_Inputs.txt') -> list:
    # Extract lines from input file
    with open(input_file) as f:
        lines = [l.strip() for l in f.readlines()]

    return lines

def Day1_Part1(input_file: str='Inputs/Day1_Inputs.txt') -> int:
    # Parse input file and extract turns
    turns = get_input(input_file)
    # Start at position 50
    d = 50
    # Count zeroes
    num_zero = 0
    for t in turns:
        # Move in given direction and wrap around at 100
        if t[0] == 'L':
            d = (d - int(t[1:]))%100
        elif t[0] == 'R':
            d = (d + int(t[1:]))%100
        else:
            raise Exception(f"Unrecognised code {t[0]}!")
        # Count zeroes
        if d == 0:
            num_zero += 1
    
    return num_zero

def Day1_Part2(input_file: str='Inputs/Day1_Inputs.txt') -> int:
    # Parse input file and extract turns
    turns = get_input(input_file)
    # Start at position 50
    d = 50
    # Count passes of zero
    num_passed_zero = 0
    # Track if we landed on zero
    at_zero = False
    for t in turns:
        # Move in given direction, but don't wrap yet
        if t[0] == 'L':
            d -= int(t[1:])
        elif t[0] == 'R':
            d += int(t[1:])
        else:
            raise Exception(f"Unrecognised code {t[0]}!")
        # Count number of multiples of 100 in given turn
        num_passed_zero += abs(d//100)
        # If turning left and landing on zero, correct for undercount
        if d <= 0 and d%100 == 0:
            num_passed_zero += 1
        # If turning left and started at zero, correct for overcount
        if t[0] == 'L' and at_zero:
            num_passed_zero -= 1
        # Update whether at zero
        if d%100 == 0:
            at_zero = True
        else:
            at_zero = False
        # Apply wrapping at 100
        d %= 100
    
    return num_passed_zero
