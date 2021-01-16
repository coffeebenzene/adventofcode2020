import time
import enum
import collections

Coord = collections.namedtuple("Coord", ["x","y"])
Side = collections.namedtuple("Sides", ["up","right","down","left"])

class Direction(enum.IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
    def opposite(self):
        return self.rotate(2)
    
    def flip(self):
        flip_map = [
            Direction.UP,
            Direction.LEFT,
            Direction.DOWN,
            Direction.RIGHT
        ]
        return flip_map[self]
    
    def rotate(self, rotations):
        return Direction((self + rotations)%4)
    
    def rotation_from(self, other):
        return Direction((other - self)%4)

class Orientation:
    def __init__(self, rotation, flipped):
        self.rotation = rotation
        self.flipped = flipped
    
    def __repr__(self):
        return f"Orientation({self.rotation}, {self.flipped})"
    
    def deorient_direction(self, oriented_direction):
        deoriented_direction = oriented_direction.rotate(-self.rotation)
        if self.flipped:
            deoriented_direction = deoriented_direction.flip()
        return Direction(deoriented_direction)

all_orientations = tuple(Orientation(r,f) for r in (0,1,2,3) for f in (False, True))

class Tile:
    def __init__(self, tiletext):
        lines = tiletext.split("\n")
        id_line = lines[0]
        id_line = id_line[5:].strip().rstrip(":")
        self.id = int(id_line)
        map = [line.strip() for line in lines[1:]]
        sides = []
        sides.append(map[0])
        sides.append("".join(x[-1] for x in map))
        sides.append(map[-1][::-1])
        sides.append("".join(x[0] for x in reversed(map)))
        self.sides = Side(*sides)
        self.reversed_sides = Side(*(x[::-1] for x in sides))
        self.interior = [line[1:-1] for line in map[1:-1]]

class OrientedTile:
    def __init__(self, tile, orientation):
        self.tile = tile
        self.orientation = orientation
    
    def __repr__(self):
        return f"OrientedTile({self.tile.id}, {self.orientation})"
    
    def get_side(self, direction, reverse=False):
        tile_direction = self.orientation.deorient_direction(direction)
        should_flip = self.orientation.flipped
        should_flip = should_flip ^ reverse
        if should_flip:
            sides = self.tile.reversed_sides
        else:
            sides = self.tile.sides
        return sides[tile_direction]
    
    def check_fit(self, direction, other_oriented_tile):
        side = self.get_side(direction)
        other_facing_side = other_oriented_tile.get_side(direction.opposite(), True)
        return side == other_facing_side
    
    def get_interior(self):
        return orient_grid(self.tile.interior, self.orientation)

class Map:
    def __init__(self, initial_tile):
        initial_oriented_tile = OrientedTile(initial_tile, Orientation(0,False))
        self.grid = {Coord(0,0): initial_oriented_tile}
        self.available_coords = set(self.get_empty_neighbours(Coord(0,0)))
    
    @staticmethod
    def get_neighbour_directions(coord):
        yield (Coord(coord.x, coord.y+1), Direction.UP)
        yield (Coord(coord.x+1, coord.y), Direction.RIGHT)
        yield (Coord(coord.x-1, coord.y), Direction.LEFT)
        yield (Coord(coord.x, coord.y-1), Direction.DOWN)
    
    def get_empty_neighbours(self, coord):
        for c,d in self.get_neighbour_directions(coord):
            if c not in self.grid:
                yield c
    
    def fit_tile(self, coord, oriented_tile):
        self.available_coords.remove(coord)
        self.grid[coord] = oriented_tile
        new_available = self.get_empty_neighbours(coord)
        self.available_coords.update(new_available)
    
    def check_fit(self, coord, oriented_tile):
        if coord not in self.available_coords:
            return
        for n_coord, n_dir in self.get_neighbour_directions(coord):
            if n_coord not in self.grid:
                continue
            n_tile = self.grid[n_coord]
            if not oriented_tile.check_fit(n_dir, n_tile):
                return False
        return True
    
    def get_boundary(self):
        x_coords, y_coords = zip(*self.grid)
        min_x = min(x_coords)
        max_x = max(x_coords)
        min_y = min(y_coords)
        max_y = max(y_coords)
        return (min_x, max_x, min_y, max_y)
    
    def get_interior(self):
        min_x, max_x, min_y, max_y = self.get_boundary()
        full_interior = []
        for y in range(max_y, min_y-1, -1): # top to bottom
            left_tile = self.grid[Coord(min_x, y)]
            row_block = left_tile.get_interior()
            for x in range(min_x+1, max_x+1): # left to right
                next_tile = self.grid[Coord(x, y)]
                for row, tile_row in zip(row_block, next_tile.get_interior()):
                    row.extend(tile_row)
            full_interior.extend(row_block)
        return full_interior

def fit_all_tiles(tiles):
    """Assumes tiles are nice.
    i.e. all sides are unique and blindly attaching any matching side will 
    fit nicely into the square
    If tiles are not nice, should use DFS/backtracking search instead.
    Also... this is still somewhat slow.
    """
    remaining_tiles = {i:tile for i,tile in enumerate(tiles)}
    initial_tile = remaining_tiles.pop(0)
    map = Map(initial_tile)
    unusable_coords = set()
    while remaining_tiles:
        for coord in list(map.available_coords):
            if coord in unusable_coords:
                continue
            
            fittable = find_fittable(map, coord, remaining_tiles)
            if fittable is None:
                unusable_coords.add(coord)
                continue
            
            idx, oriented_tile = fittable
            map.fit_tile(coord, oriented_tile)
            remaining_tiles.pop(idx)
    return map

def find_fittable(map, coord, remaining_tiles):
    for idx, tile in remaining_tiles.items():
        for orient in all_orientations:
            oriented_tile = OrientedTile(tile, orient)
            if map.check_fit(coord, oriented_tile):
                return (idx, oriented_tile)
    return None

def orient_grid(grid, orientation):
    if orientation.flipped:
        grid = [row[::-1] for row in grid]
    for i in range(orientation.rotation):
        grid = [x for x in zip(*reversed(grid))]
    return [list(x) for x in grid]


class SeaMonster:
    def __init__(self, monster_shape):
        self.shape = monster_shape
        self.head_index = monster_shape[0].index("#")
        self.offsets = []
        for i, line in enumerate(monster_shape):
            for j, char in enumerate(line, -self.head_index):
                if char == "#":
                    self.offsets.append((i, j))
        self.length = len(monster_shape[0])
        self.height = len(monster_shape)
        self.size = sum(line.count("#") for line in monster_shape)
    
    def position_is_head(self, grid, i, j):
        for offset_i, offset_j in self.offsets:
            if grid[i+offset_i][j+offset_j] != "#":
                return False
        return True
    

def count_sea_monster(map, monster):
    height = len(map) - (monster.height - 1)
    width = len(map[0]) - (monster.length - 1 - monster.head_index)
    count = 0
    for i in range(height):
        j = monster.head_index
        while j < width:
            if monster.position_is_head(map, i, j):
                count += 1
                j += monster.length
            else:
                j += 1
    return count

def compute_part1(map):
    min_x, max_x, min_y, max_y = map.get_boundary()
    product = 1
    corners = [
        Coord(min_x, min_y),
        Coord(max_x, min_y),
        Coord(min_x, max_y),
        Coord(max_x, max_y),
    ]
    for c in corners:
        product *= map.grid[c].tile.id
    return product

def compute_part2(map):
    interior = map.get_interior()
    monster = SeaMonster([
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ])
    
    for orient in all_orientations:
        oriented_interior = orient_grid(interior, orient)
        count = count_sea_monster(oriented_interior, monster)
        if count == 0:
            continue
        total_roughs = sum(line.count("#") for line in interior)
        total_monster_size = monster.size * count
        return total_roughs - total_monster_size
    
    return None

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        tiles = [Tile(t) for t in f.read().strip().split("\n\n")]
    
    map = fit_all_tiles(tiles)
    product = compute_part1(map)
    print(f"Part 1: product: {product}")
    
    roughness = compute_part2(map)
    print(f"Part 2: roughness: {roughness}")
    
    end = time.time()
    print(f"Took {end - start}s")
