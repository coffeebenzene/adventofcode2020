import collections
import time

Coord = collections.namedtuple("Coord", ["row","col"])

def generate_path(boundary, slope):
    current = Coord(0,0)
    yield current
    while True:
        new_row = current.row + slope.row
        new_col = (current.col + slope.col) % boundary.col
        if new_row >= boundary.row:
            break
        current = Coord(new_row, new_col)
        yield current

def count_trees(map, slope):
    boundary = Coord(len(map),len(map[0]))
    count = 0
    for coord in generate_path(boundary, slope):
        if map[coord.row][coord.col] == "#":
            count += 1
    return count

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        map = [line.strip() for line in f.readlines()]
    
    tree_count13 = count_trees(map, Coord(1,3))
    print(f"part1: count: {tree_count13}")
    
    tree_count_total = tree_count13
    for slope in [Coord(1,1), Coord(1,5), Coord(1,7), Coord(2,1)]:
        tree_count_total *= count_trees(map, slope)
    print(f"part2: count: {tree_count_total}")
    
    end = time.time()
    print(f"Took {end - start}s")
