import collections
import functools
import itertools
import time

Coord = collections.namedtuple("Coord3d", ["x","y","z","w"], defaults=[0,0])

def preprocess_state(data):
    active_cubes = set()
    for i, line in enumerate(data):
        for j, cell in enumerate(line):
            if cell == "#":
                active_cubes.add(Coord(i,j))
    return active_cubes

@functools.lru_cache(maxsize=None)
def get_neighbourhood(c, dims):
    neighbourhood = set()
    for offset in itertools.product((-1,0,1), repeat=dims):
        coord_vals = (x+y for x,y in zip(c, offset))
        n_coord = Coord(*coord_vals)
        neighbourhood.add(n_coord)
    return frozenset(neighbourhood)

def is_cube_active_in_next_state(active_cubes, cube, dims):
    neighbours = get_neighbourhood(cube, dims) - {cube}
    active_neighbour_count = len(active_cubes & neighbours)
    return active_neighbour_count == 3 or (cube in active_cubes and active_neighbour_count == 2)

def next_state(active_cubes, dims):
    processed_cubes = set()
    new_active_cubes = set()
    for cube in active_cubes:
        neighbourhood = get_neighbourhood(cube, dims)
        neighbourhood = [n for n in neighbourhood if n not in processed_cubes]
        for cube in neighbourhood:
            if is_cube_active_in_next_state(active_cubes, cube, dims):
                new_active_cubes.add(cube)
            processed_cubes.add(cube)
    return new_active_cubes

def str_state3d(active_cubes):
    min_dims = list(next(iter(active_cubes)))
    max_dims = min_dims.copy()
    for cube in active_cubes:
        for dim in range(3):
            dim_val = cube[dim]
            if dim_val < min_dims[dim]:
                min_dims[dim] = dim_val
            if dim_val > max_dims[dim]:
                max_dims[dim] = dim_val
    
    text = ["-"*40, f"min_dims: {min_dims} | max_dims: {max_dims} | x↓ y→ z↓↓"]
    
    for z in range(min_dims[2], max_dims[2]+1):
        slice = []
        for x in range(min_dims[0], max_dims[0]+1):
            row = []
            for y in range(min_dims[1], max_dims[1]+1):
                row.append("#" if Coord(x,y,z) in active_cubes else ".")
            slice.append("".join(row))
        text.append(f"\nz = {z}:")
        text.extend(slice)
    return "\n".join(text)

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        data = f.readlines()
    
    active_cubes = preprocess_state(data)
    for i in range(6):
        active_cubes = next_state(active_cubes, 3)
    print(f"part1: active cubes = {len(active_cubes)}")
    
    active_cubes = preprocess_state(data)
    for i in range(6):
        active_cubes = next_state(active_cubes, 4)
    print(f"part2: active cubes = {len(active_cubes)}")
    
    end = time.time()
    print(f"Took {end - start}s")
