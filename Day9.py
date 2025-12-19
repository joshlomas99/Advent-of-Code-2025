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

def get_input(input_file: str='Inputs/Day9_Inputs.txt') -> list:
    # Extract tile coordinates from input file
    with open(input_file) as f:
        tiles = [tuple(int(i) for i in l.strip().split(',')) for l in f.readlines()]

    return tiles

@time_function
def Day9_Part1(input_file: str='Inputs/Day9_Inputs.txt') -> int:
    # Parse input file and extract tile coordinates
    tiles = get_input(input_file)

    # Track maximum area found
    max_area = 0
    # Loop over tiles
    for i in range(len(tiles)):
        # Loop over tiles beyond this tile in the list, to avoid repetition
        for j in range(i+1, len(tiles)):
            # Calculate area of polygon formed with these tiles as the opposite corners
            area = (abs(tiles[i][0] - tiles[j][0])+1)*(abs(tiles[i][1] - tiles[j][1])+1)
            # If this is bigger than current max, overwrite value
            if area > max_area:
                max_area = 1*area
    
    return max_area

def crosses_border_num_horiz(edge_y, edge_bounds_x, vert_borders):
    # Calculate the number of vertical borders fully crossed by a horizontal edge, defined as a
    # y coordinate and two x bounds
    num_crossed = 0
    # Loop over vertical borders
    for border_x, border_bounds_y in vert_borders:
        # Check for crossing
        crosses_vert = edge_bounds_x[0] < border_x and border_x < edge_bounds_x[1]
        crosses_horiz = border_bounds_y[0] < edge_y and edge_y < border_bounds_y[1]
        # If found, count
        if crosses_vert and crosses_horiz:
            num_crossed += 1

    return num_crossed

def crosses_border_num_vert(edge_x, edge_bounds_y, horiz_borders):
    # Calculate the number of horizontal borders fully crossed by a vertical edge, defined as an
    # x coordinate and two y bounds
    num_crossed = 0
    # Loop over horizontal borders
    for border_y, border_bounds_x in horiz_borders:
        # Check for crossing
        crosses_horiz = edge_bounds_y[0] < border_y and border_y < edge_bounds_y[1]
        crosses_vert = border_bounds_x[0] < edge_x and edge_x < border_bounds_x[1]
        # If found, count
        if crosses_vert and crosses_horiz:
            num_crossed += 1

    return num_crossed

def touches_border_horiz(tile1, tile2, vert_borders):
    # Calculate whether either of the two horizontal edges of a rectangle defined by two tiles giving
    # the coordinates of the opposite corners, touch any vertical borders
    # Define the two edges as y coordinates and two x bounds
    x_bounds = sorted((tile1[0], tile2[0]))
    for edge_y, edge_bounds_x in [(tile1[1], x_bounds), (tile2[1], x_bounds)]:
        # Loop over vertical borders
        for border_x, border_bounds_y in vert_borders:
            # Check for contact
            crosses_vert = border_bounds_y[0] <= border_x and border_x <= border_bounds_y[1]
            crosses_horiz = border_bounds_y[0] <= edge_y and edge_y <= border_bounds_y[1]
            # If found, return True
            if crosses_vert and crosses_horiz:
                return True

    # If nothing was found, return False
    return False

def touches_border_vert(tile1, tile2, horiz_borders):
    # Calculate whether either of the two vertical edges of a rectangle defined by two tiles giving
    # the coordinates of the opposite corners, touch any horizontal borders
    # Define two edges as x coordinates and two y bounds
    y_bounds = sorted((tile1[1], tile2[1]))
    for edge_x, edge_bounds_y in [(tile1[0], y_bounds), (tile2[0], y_bounds)]:
        # Loop over horizontal borders
        for border_y, border_bounds_x in horiz_borders:
            # Check for contact
            crosses_horiz = edge_bounds_y[0] <= border_y and border_y <= edge_bounds_y[1]
            crosses_vert = border_bounds_x[0] <= edge_x and edge_x <= border_bounds_x[1]
            # If found, return True
            if crosses_vert and crosses_horiz:
                return True

    # If nothing was found, return False
    return False

def touches_border(tile1, tile2, vert_borders, horiz_borders):
    # Checks for contact with borders on any edge of a rectangle defined by two tiles giving
    # the coordinates of the opposite corners
    if touches_border_horiz(tile1, tile2, vert_borders): # Check horizontal edges
        return True
    if touches_border_vert(tile1, tile2, horiz_borders): # Check vertical edges
        return True
    return False
    
from matplotlib import pyplot as plt

@time_function
def Day9_Part2(input_file: str='Inputs/Day9_Inputs.txt') -> int:
    # Parse input file and extract tile coordinates
    tiles = get_input(input_file)
    tile_bounds = ((min(t[0] for t in tiles)-1, max(t[0] for t in tiles)+1),
                   (min(t[1] for t in tiles)-1, max(t[1] for t in tiles)+1))

    # Find vertical and horizontal borders defined by adjacent tiles in the list
    vert_borders, horiz_borders = [], []
    for i in range(len(tiles)):
        # Compare current and next tiles
        tile1, tile2 = tiles[i], tiles[(i+1)%len(tiles)]
        # Check for change in each coordinate
        dtile = (tile1[0] - tile2[0], tile1[1] - tile2[1])
        if all(dtile): # Cannot have a change in both coords (no diagonal borders)
            raise Exception("Non-orthogonal border detected!")
        # If change in y, vertical border found, define by single x coordinate and y bounds
        if dtile[1]:
            vert_borders.append((tile1[0], sorted((tile1[1], tile2[1]))))
        # Else change in x, horizontal border found, define by single y coordinate and x bounds
        else:
            horiz_borders.append((tile1[1], sorted((tile1[0], tile2[0]))))

    # Define a new set of tiles, to form a second layer of borders around the outside of the
    # initial polygon
    outer_tiles = []
    # inner_tiles = []
    # Loop through tiles
    for i in range(len(tiles)):
        # Determine the diagonal direction which is opposite to the two edges connecting to this tile
        parity = ((tiles[i][0] - tiles[(i-1)%len(tiles)][0]) + (tiles[i][0] - tiles[(i+1)%len(tiles)][0]),
                  (tiles[i][1] - tiles[(i-1)%len(tiles)][1]) + (tiles[i][1] - tiles[(i+1)%len(tiles)][1]))
        # Convert to +/- 1 in each direction
        parity = ((parity[0] > 0)*2 - 1, (parity[1] > 0)*2 - 1)
        # Define tile one diagonal step outside the shape from this tile
        outer_tile = (tiles[i][0] + parity[0], tiles[i][1] + parity[1])

        # Check number of vertical borders crossed by a line from this "outer" tile to the maximum
        # x coordinate of the polygon
        num_crossed = crosses_border_num_horiz(outer_tile[1], [outer_tile[0], tile_bounds[0][1]], vert_borders)

        # If this is odd the "outer" tile is actually inside the polygon, even means it was outside
        if num_crossed%2:
            # inner_tiles.append(outer_tile)
            # Redefine outer tile in the opposite direction to before, must now be outside
            outer_tile = (tiles[i][0] - parity[0], tiles[i][1] - parity[1])

        # Create list of outer tiles
        outer_tiles.append(outer_tile)
    
    # Find outer vertical and horizontal borders wrapping around polygon, defined by adjacent tiles
    # in the list of outer tiles, as before
    outer_vert_borders, outer_horiz_borders = [], []
    for i in range(len(outer_tiles)):
        outer_tile1, outer_tile2 = outer_tiles[i], outer_tiles[(i+1)%len(outer_tiles)]
        douter_tile = (outer_tile1[0] - outer_tile2[0], outer_tile1[1] - outer_tile2[1])
        if all(douter_tile):
            raise Exception("Non-orthogonal border detected!")
        if douter_tile[1]:
            outer_vert_borders.append((outer_tile1[0], sorted((outer_tile1[1], outer_tile2[1]))))
        else:
            outer_horiz_borders.append((outer_tile1[1], sorted((outer_tile1[0], outer_tile2[0]))))

    # Find areas of rectangles formed by all possible combinations of tiles in the list
    areas = []
    # Loop over tiles
    for i in range(len(tiles)):
        # Loop over tiles beyond this tile in the list, to avoid repetition
        for j in range(i+1, len(tiles)):
            # Calculate area of polygon formed with these tiles as the opposite corners
            area = (abs(tiles[i][0] - tiles[j][0])+1)*(abs(tiles[i][1] - tiles[j][1])+1)
            # Add tiles and corresponding area to list
            areas.append(((tiles[i], tiles[j]), area))

    # Sort by area, largest first, so we can stop once we find any which don't cross any edges
    areas = sorted(areas, key=lambda x: x[1], reverse=True)
    
    # Verify that no rectangle edges touch any outer borders of the polygon
    for (tile1, tile2), area in areas:
        if touches_border(tile1, tile2, outer_vert_borders, outer_horiz_borders):
            continue
        # When found, break loop with current tiles and area
        else:
            break

    # Plot showing polygon, red and green tiles and largest possible rectangle
    fig = plt.figure(figsize=[10, 10])
    ax = fig.add_subplot(1, 1, 1)
    x, y = [t[0] for t in tiles + [tiles[0]]], [t[1] for t in tiles + [tiles[0]]]
    ax.plot(x, y, color='r', lw=3, zorder=2)
    ax.fill(x, y, color=[0.1, 0.9, 0.3], zorder=0)
    # ax.scatter([t[0] for t in outer_tiles], [t[1] for t in outer_tiles], color=[1.0, 0.8, 0.3], s=500, zorder=50)
    # ax.scatter([t[0] for t in inner_tiles], [t[1] for t in inner_tiles], color=[0.5, 0, 1], s=500, zorder=50)
    square_borders = [tile1[0], tile1[0], tile2[0], tile2[0]], [tile1[1], tile2[1], tile2[1], tile1[1]]
    ax.fill(*square_borders, color=[0.0, 0.6, 1], zorder=1)
    ax.scatter(*square_borders, color='b', marker='X', s=250, zorder=3)
    ax.fill([tile_bounds[0][0], tile_bounds[0][0], tile_bounds[0][1], tile_bounds[0][1]],
            [tile_bounds[1][0], tile_bounds[1][1], tile_bounds[1][1], tile_bounds[1][0]],
            color='k', alpha=0.1)
    plt.show()

    return area
