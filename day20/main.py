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

class Tile:
    def __init__(self, tiletext):
        lines = tiletext.split("\n")
        id_line = lines[0]
        id_line = id_line[5:].strip().rstrip(":")
        self.id = int(id_line)
        self.map = [line.strip() for line in lines[1:]]
        sides = []
        sides.append(self.map[0])
        sides.append("".join(x[-1] for x in self.map))
        sides.append(self.map[-1][::-1])
        sides.append("".join(x[0] for x in reversed(self.map)))
        self.sides = Side(*sides)
        self.reversed_sides = Side(*(x[::-1] for x in sides))
    
    def find_fit_orientations(self, direction, other_tile):
        side = self.sides[direction]
        for orientations in get_fits(side, direction, other_tile):
            yield orientations

class OrientedTile:
    def __init__(self, tile, orientation):
        self.tile = tile
        self.orientation = orientation
    
    def get_side(self, direction):
        tile_direction = self.orientation.deorient_direction(direction)
        if self.orientation.flipped:
            sides = self.tile.reversed_sides
        else:
            sides = self.tile.sides
        return sides[tile_direction]
    
    def find_fit_orientations(self, direction, other_tile):
        side = self.get_side(direction)
        for orientations in get_fits(side, direction, other_tile):
            yield orientations

# TODO: Refactor logic
# find more meaningful way to compute orientations that is still efficient.
# possibly try to find out how orientations interact with each other.
def get_fits(side, direction, other_tile):
    other_tile_wanted_direction = direction.opposite()
    for other_direction, other_side in zip(Direction, other_tile.reversed_sides):
        if side == other_side:
            rotations = other_tile_wanted_direction.rotation_from(other_direction)
            yield Orientation(rotations, False)
    
    other_tile_wanted_direction = other_tile_wanted_direction.flip()
    for other_direction, other_side in zip(Direction, other_tile.sides):
        if side == other_side:
            rotations = other_tile_wanted_direction.rotation_from(other_direction)
            yield Orientation(rotations, True)

class Map:
    def __init__(self, initial_tile):
        initial_oriented_tile = OrientedTile(initial_tile, Orientation(0,False))
        self.map = {Coord(0,0): initial_oriented_tile}
        self.available_coords = set(self.get_empty_neighbours(Coord(0,0)))
    
    @staticmethod
    def get_neighbours(coord):
        for i in (-1,1):
            for j in (-1,1):
                yield Coord(coord.x+i, coord.y+j)
    
    def get_empty_neighbours(self, coord):
        for c in self.get_neighbours(coord):
            if c not in self.map:
                yield c
    
    def fit_tile(self, coord, oriented_tile):
        self.available_coords.remove(coord)
        self.map[coord] = oriented_tile
        new_available = self.get_empty_neighbours(coord)
        self.available_coords.update(new_available)
    
    def find_fits(self, coord, tile):
        if coord not in self.available_coords:
            return
        pass

if __name__ == "__main__":
    start = time.time()
    
    with open("testinput.txt") as f:
        tiles = [Tile(t) for t in f.read().strip().split("\n\n")]
    
    o = OrientedTile(tiles[3], Orientation(2,True))
    for d in Direction:
        for t in tiles:
            if t.id != o.tile.id:
                for possible_o in o.check_fit_orientation(d, t):
                    print(f"{o.tile.id}_{o.orientation} @ {d} fits {t.id} @ {possible_o}")
    
    for i,t1 in enumerate(tiles):
        for d in Direction:
            for j,t2 in enumerate(tiles):
                if j == i:
                    continue
                for possible_o in t1.check_fit_orientation(d, t2):
                    print(f"{t1.id} @ {d} fits {t2.id} at @ {possible_o}")
    
    with open("input.txt") as f:
        tiles = [Tile(t) for t in f.read().strip().split("\n\n")]
    
    Map(tiles.pop())
    print(tiles[0].sides)
    print(len(tiles))
    
    print(f"Part 1: valid messages: ")
    print(f"Part 2: valid messages: ")
    
    end = time.time()
    print(f"Took {end - start}s")
