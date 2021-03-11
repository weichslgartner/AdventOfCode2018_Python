# import cProfile
from collections import namedtuple
from functools import lru_cache
from typing import List


class Point(namedtuple('Point', 'w x y z')):
    def __repr__(self):
        return f'{self.w} {self.y} {self.x} {self.z}'

    def __hash__(self):
        return hash(self.w) ^ hash(self.x) ^ hash(self.y) ^ hash(self.z)

    def __eq__(self, other):
        return self.w == other.w and self.x == other.x and self.y == other.y and self.z == other.z

    @lru_cache(None)
    def manhattan_distance(self, other):
        return abs(self.w - other.w) + abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


def solve(points: List[Point]):
    constellations = {}
    const_dict = {}
    for i, p in enumerate(points[:-1]):
        if p not in const_dict:
            constellations[i] = [p]
            const_dict[p] = i
        for p2 in points[i + 1:]:
            if p.manhattan_distance(p2) <= 3:
                constellations[const_dict[p]].append(p2)
                if p2 in const_dict and const_dict[p] != const_dict[p2]:
                    merge_constellations(const_dict, constellations, p, p2)
                else:
                    const_dict[p2] = const_dict[p]
    return len(constellations)


def merge_constellations(const_dict, constellations, p, p2):
    old_idx = const_dict[p]
    for pc in constellations[old_idx]:
        const_dict[pc] = const_dict[p2]
        constellations[const_dict[p2]].append(pc)
    del constellations[old_idx]


def parse_input(file_name: str) -> List[Point]:
    points = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            w, x, y, z = line.split(",")
            points.append(Point(int(w), int(x), int(y), int(z)))
    return points


def main():
    assert solve(parse_input("../inputs/input_25_test.txt")) == 2, "test 0"
    assert solve(parse_input("../inputs/input_25_test1.txt")) == 4, "test 0"
    assert solve(parse_input("../inputs/input_25_test2.txt")) == 3, "test 2"
    assert solve(parse_input("../inputs/input_25_test3.txt")) == 8, "test 3"
    print("Part 1: ", solve(parse_input("../inputs/input_25.txt")))


if __name__ == "__main__":
    main()
