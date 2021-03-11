# import cProfile
from collections import namedtuple
from functools import lru_cache
from typing import List


class Point(namedtuple('Point', 'x y z')):
    def __repr__(self):
        return f'{self.y} {self.x} {self.z}'

    def __hash__(self):
        return hash(self.x) ^ hash(self.y) ^ hash(self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    @lru_cache(None)
    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


class Nanobot(namedtuple('Nanobot', 'point r')):
    def __repr__(self):
        return f'P={self.point} r={self.r}'


def parse_input(file_name: str) -> List:
    points = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            tokenz = line.split(",")
            x = tokenz[0].split("<")[1]
            y = tokenz[1]
            z = tokenz[2].split(">")[0]
            r = tokenz[3].split("=")[1].strip()
            points.append(Nanobot(Point(int(x), int(y), int(z)), int(r)))
    return points


def part_1(nanobots):
    sbot = max(nanobots, key=lambda x: x[1])
    n_bots_range = sum(n.point.manhattan_distance(sbot.point) <= sbot.r for n in nanobots)
    return n_bots_range


def main():
    nanobots = parse_input("../inputs/input_23.txt")
    n_bots_range = part_1(nanobots)
    print("Part 1", n_bots_range)


if __name__ == "__main__":
    main()
