# import cProfile
from collections import namedtuple
from functools import lru_cache
from typing import List

from z3 import Ints, Optimize, Int, Sum, If, set_param, ArithRef

set_param('parallel.enable', True)


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


def num_in_range(nanobots: List[Nanobot], sbot: Nanobot):
    return sum(n.point.manhattan_distance(sbot.point) <= sbot.r for n in nanobots)


def part_1(nanobots: List[Nanobot]) -> int:
    sbot = max(nanobots, key=lambda x: x[1])
    n_bots_range = num_in_range(nanobots, sbot)
    return n_bots_range


def zabs(x: ArithRef):
    return If(x > 0, x, -x)


def z_manhattan(x: ArithRef, y: ArithRef, z: ArithRef, p: Point):
    return zabs(x - p.x) + zabs(y - p.y) + zabs(z - p.z)


def part_2(nanobots: List[Nanobot]) -> int:
    x, y, z = Ints("x y z")
    opt = Optimize()
    bot_cond = []
    for i, bot in enumerate(nanobots):
        cond = Int(f"bot_{i}")
        bot_cond.append(cond)
        opt.add(cond == If(z_manhattan(x, y, z, bot.point) <= bot.r, 1, 0))
    overlaps = Sum(bot_cond)
    dist_zero = Int('dist_zero')
    opt.add(dist_zero == z_manhattan(x, y, z, Point(0, 0, 0)))
    _ = opt.maximize(overlaps)
    dist = opt.maximize(dist_zero)
    opt.check()
    return dist.upper()


def main():
    nbots = parse_input("../inputs/input_23.txt")
    print("Part 1:", part_1(nbots))
    print("Part 2:", part_2(nbots))


if __name__ == "__main__":
    main()
