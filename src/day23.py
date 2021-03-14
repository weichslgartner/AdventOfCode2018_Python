# import cProfile
import random
from collections import namedtuple, defaultdict
from functools import lru_cache
from math import exp
from random import shuffle
from typing import List

from z3 import *

set_param('parallel.enable', True)


class Point(namedtuple('Point', 'x y z')):
    def __repr__(self):
        return f'{self.y} {self.x} {self.z}'

    def __hash__(self):
        return hash(self.x) ^ hash(self.y) ^ hash(self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def rand_neighbor(self):
        l = [1, 0, 0]
        sign_list = [-1, 1]
        shuffle(l)
        shuffle(sign_list)
        sign = sign_list[0]
        return Point(self.x + sign * l[0], self.y + sign * l[1], self.z + sign * l[2])

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


def point_in_range(nanobots: List[Nanobot], point: Point):
    return sum(n.point.manhattan_distance(point) <= n.r for n in nanobots)


def part_1(nanobots: List[Nanobot]) -> int:
    sbot = max(nanobots, key=lambda x: x[1])
    n_bots_range = num_in_range(nanobots, sbot)
    return n_bots_range


def part_2_old(nanobots):
    p = Point(12, 10, 12)
    best_point = p
    best = point_in_range(nanobots, p)
    f_x = best
    temperature = 500
    for _ in range(1000000):
        p_new = p.rand_neighbor()
        f_y = point_in_range(nanobots, p)
        print(p_new, temperature)

        if f_y > f_x or random.uniform(0, 1) < exp(-(f_y - f_x) / temperature):
            f_x = f_y
            p = p_new
        if f_y > best:
            best = f_y
            best_point = p_new
        print(f_y, best)
        temperature *= 0.99999
    print(best_point)


def part_2_bounds(nanobots: Nanobot, bounds=10):
    best_val = 0
    best_point = None
    checked = set()
    res = None
    for bot in nanobots:
        p = bot.point
        for x in range(-bounds, bounds):
            for y in range(-bounds, bounds):
                for z in range(-bounds, bounds):
                    new_point = Point(p.x + x, p.y + y, p.z + z)
                    if new_point not in checked:
                        checked.add(new_point)
                        f_y = point_in_range(nanobots, new_point)
                        if f_y > best_val:
                            best_val = f_y
                            new_manhattan = new_point.manhattan_distance(Point(0, 0, 0))
                            if res is None or new_manhattan < res:
                                best_point = new_point
                                res = new_manhattan

    print(best_val, best_point)
    return res


def part_2_dic(nanobots: Nanobot):
    point_dict = defaultdict(set)
    best = 0
    best_point = None
    for i, bot in enumerate(nanobots):
        radius = bot.r
        p = bot.point
        for x in range(-radius, radius):
            for y in range(-radius, radius):
                for z in range(-radius, radius):
                    if abs(x) + abs(y) + abs(z) > radius:
                        continue
                    new_point = Point(p.x + x, p.y + y, p.z + z)
                    point_dict[new_point].add(i)
                    if len(point_dict[new_point]) > best:
                        best = len(point_dict[new_point])
                        best_point = new_point
    print(best_point, best)


def zabs(x: ArithRef):
    return If(x > 0, x, -x)


def z_manhattan(x: ArithRef, y: ArithRef, z: ArithRef, p: Point):
    return zabs(x - p.x) + zabs(y - p.y) + zabs(z - p.z)


def part_2(nanobots: List[Nanobot]) -> int:
    x, y, z = Ints("x y z")
    opt = Optimize()
    circles = []
    for i, bot in enumerate(nanobots):
        cond = Int(f"bot_{i}")
        circles.append(cond)
        opt.add(cond == If(z_manhattan(x, y, z, bot.point) <= bot.r, 1, 0))
    overlaps = Sum(circles)
    dist_zero = Int('dist_zero')
    opt.add(dist_zero == z_manhattan(x, y, z, Point(0, 0, 0)))
    ov = opt.maximize(overlaps)
    dist = opt.maximize(dist_zero)
    opt.check()
    return dist.upper()


def main():
    nbots = parse_input("../inputs/input_23.txt")
    n_bots_range = part_1(nbots)
    print("Part 1", n_bots_range)
    print("Part 2", part_2(nbots))


if __name__ == "__main__":
    main()
