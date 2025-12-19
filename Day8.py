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

def get_input(input_file: str='Inputs/Day8_Inputs.txt') -> list:
    # Extract box coordinates from input file
    with open(input_file) as f:
        boxes = [tuple(int(i) for i in l.strip().split(',')) for l in f.readlines()]

    # Determine distances between each box and every other box and store in dict
    dist_to_box = dict()
    for n in range(len(boxes)):
        dist_to_box[boxes[n]] = []
        for m in range(len(boxes)):
            if n == m:
                continue
            dist = sum((ai - bi)**2 for ai, bi in zip(boxes[n], boxes[m]))
            dist_to_box[boxes[n]].append((boxes[m], dist))
        # Sort distances for each box, smallest first
        dist_to_box[boxes[n]] = sorted(dist_to_box[boxes[n]], key=lambda x: x[1])

    return boxes, dist_to_box

import operator
from functools import reduce

@time_function
def Day8_Part1(input_file: str='Inputs/Day8_Inputs.txt') -> int:
    # Parse input file and extract box coordinates and distances between boxes
    boxes, dist_to_box = get_input(input_file)

    connections = 0
    # Assign circuit index to each box
    circuits = {b: n for n, b in enumerate(boxes)}
    # Until 1000 connections are made
    while connections < 1000:
        # Find box with shortest distance to closest neighbour
        closest_box = min(boxes, key=lambda b: dist_to_box[b][0][1])
        # Get closest neighbour
        neighbour = dist_to_box[closest_box][0][0]
        # Remove pair from each other's distance list
        for b in [closest_box, neighbour]:
            dist_to_box[b].pop(0)
        # If they were not in the same circuit already
        if circuits[closest_box] != circuits[neighbour]:
            joined_circuit = min(circuits[closest_box], circuits[neighbour])
            removed_circuit = max(circuits[closest_box], circuits[neighbour])
            # Assign the same circuit index to all boxes in both circuits
            for cb in [cb for cb, n in circuits.items() if n == removed_circuit]:
                circuits[cb] = joined_circuit
        connections += 1

    # Determine sizes of all circuits
    all_circuits = list(circuits.values())
    circuit_sizes = sorted([all_circuits.count(size) for size in set(all_circuits)], reverse=True)

    # Find product of top three
    return reduce(operator.mul, circuit_sizes[:3])

@time_function
def Day8_Part2(input_file: str='Inputs/Day8_Inputs.txt') -> int:
    # Parse input file and extract box coordinates and distances between boxes
    boxes, dist_to_box = get_input(input_file)

    connections = 0
    # Assign circuit index to each box
    circuits = {b: n for n, b in enumerate(boxes)}
    # Until there is only one circuit
    while len(set(circuits.values())) > 1:
        # Find box with shortest distance to closest neighbour
        closest_box = min(boxes, key=lambda b: dist_to_box[b][0][1])
        # Get closest neighbour
        neighbour = dist_to_box[closest_box][0][0]
        # Remove pair from each other's distance list
        for b in [closest_box, neighbour]:
            dist_to_box[b].pop(0)
        # If they were not in the same circuit already
        if circuits[closest_box] != circuits[neighbour]:
            joined_circuit = min(circuits[closest_box], circuits[neighbour])
            removed_circuit = max(circuits[closest_box], circuits[neighbour])
            # Assign the same circuit index to all boxes in both circuits
            for cb in [cb for cb, n in circuits.items() if n == removed_circuit]:
                circuits[cb] = joined_circuit
        connections += 1

    # Multiply x-coordinates of final two connected boxes
    return closest_box[0]*neighbour[0]

def find(x, graph):
    if graph[x] == x:
        return x
    else:
        return find(graph[x], graph)

def union(x, y, graph):
    graph[find(y, graph)] = find(x, graph)

    return graph

# input_file: str='Inputs/Day8_Inputs.txt'
# # Parse input file and extract box coordinates
# boxes, dist_to_box = get_input(input_file)

# circuits = {b: b for b in boxes}

# connections = 0
# while connections < 1000:
#     # Find closest pair of boxes
#     box1, box2 = dist_to_box.pop(0)[0]
#     circuits = union(box1, box2, circuits)
#     connections += 1

# # Determine sizes of all circuits
# all_circuits = list(find(b, circuits) for b in boxes)
# circuit_sizes = sorted([all_circuits.count(size) for size in set(all_circuits)], reverse=True)

# # Find product of top three
# print(reduce(operator.mul, circuit_sizes[:3]))
