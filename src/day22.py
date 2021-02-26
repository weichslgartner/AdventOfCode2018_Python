import sys
from collections import namedtuple, defaultdict
import cProfile
import dataclasses
from enum import Enum, IntEnum
from typing import Set, List
from queue import PriorityQueue
from functools import lru_cache


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.y} {self.x}'

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


class RegionType(IntEnum):
    ROCKY = 0,
    WET = 1,
    NARROW = 2


class Tool(Enum):
    TORCH = 1,
    NEITHER = 2,
    CLIMBING_GEAR = 3


@dataclasses.dataclass(order=True)
class Element(object):
    tool: Tool = dataclasses.field(compare=False)
    point: Point = dataclasses.field(compare=False)
    # cost: int  = dataclasses.field(compare=False)
    priority: int

    def __hash__(self):
        return hash(self.tool) ^ hash(self.point)

    def __eq__(self, other):
        return self.tool == other.tool and self.point == other.point


class Day22:
    def __init__(self, depth: int, target: Point):
        self.depth = depth
        self.target = target
        self.max_x = 0
        self.max_y = 0
        self.erosion_levels = {}

    @lru_cache(None)
    def geologic_index(self, p: Point) -> int:
        if p == Point(0, 0) or p == self.target:
            return 0
        elif p.y == 0:
            return p.x * 16807
        elif p.x == 0:
            return p.y * 48271
        return self.erosion_levels[Point(p.x - 1, p.y)] * self.erosion_levels[Point(p.x, p.y - 1)]

    @lru_cache(None)
    def erosion_level(self, p: Point) -> int:
        if p not in self.erosion_levels.keys():
            if Point(p.x - 1, p.y) not in self.erosion_levels.keys() and p.x > 0:
                for x in range(self.max_x):
                    self.erosion_level(Point(x, p.y))
            if Point(p.x, p.y - 1) not in self.erosion_levels.keys() and p.y > 0:
                for y in range(self.max_y):
                    self.erosion_level(Point(p.x, y))
            self.erosion_levels[p] = (self.geologic_index(p) + self.depth) % 20183
        if p.x > self.max_x:
            self.max_x = p.x
        if p.y > self.max_y:
            self.max_y = p.y
        return self.erosion_levels[p]

    @lru_cache(None)
    def ground(self, p: Point) -> RegionType:
        return RegionType(self.erosion_level(p) % 3)

    @property
    def eval_risk_level(self, print_output: bool = False) -> int:
        risk_level = 0
        for y in range(self.target.y + 1):
            for x in range(self.target.x + 1):
                ground = self.ground(Point(x=x, y=y))
                c = '.'
                if ground == 1:
                    c = '='
                elif ground == 2:
                    c = '|'
                if print_output:
                    print(c, end="")
                risk_level += ground

            if print_output:
                print()
        return risk_level


def get_neighbors(p: Point) -> List[Point]:
    neighbors = []
    for p in [Point(p.x + 1, p.y), Point(p.x, p.y - 1), Point(p.x, p.y + 1), Point(p.x - 1, p.y)]:
        if p.x >= 0 and p.y >= 0:
            neighbors.append(p)
    return neighbors


reg_to_tool = {
    RegionType.ROCKY: {Tool.TORCH, Tool.CLIMBING_GEAR},
    RegionType.WET: {Tool.NEITHER, Tool.CLIMBING_GEAR},
    RegionType.NARROW: {Tool.NEITHER, Tool.TORCH}
}

@lru_cache(None)
def change_tool(rtype_new: RegionType, rtype_old: RegionType, cur_tool: Tool) -> [bool, List[Tool]]:
    if cur_tool in reg_to_tool[rtype_new]:
        return False, []
    return True, reg_to_tool[rtype_new] & reg_to_tool[rtype_old]


def main():
    day22 = Day22(depth=510, target=Point(10, 10))
    day22 = Day22(depth=7305, target=Point(13, 734))
    print(day22.eval_risk_level)
    p_queue = PriorityQueue()
    start = Element(Tool.TORCH, Point(0, 0), 0)
    p_queue.put(Element(Tool.TORCH, Point(0, 0), day22.target.manhattan_distance(Point(0, 0)) * 7))
    best_cost = 1022  # sys.maxsize # 1034 # 995 wrong
    visited_two = defaultdict(int)
    cost_so_far = dict()
    cost_so_far[start] = 0
    i = 0
    f = open('debug.csv', mode="w")
    while not p_queue.empty():
        cur: Element = p_queue.get()
        visited_two[cur.point] += 1
        f.write(f"{cur.point.x},{cur.point.y},{visited_two[cur.point]}\n")
        #if i == 10000:
        #    print(cur.point, cost_so_far[cur], cur.tool, p_queue.qsize())
        #    i = 0

        if cur.point == day22.target and cost_so_far[cur] < best_cost:
            if cur.tool == Tool.TORCH:
                best_cost = cost_so_far[cur]
                print("found with costs ", best_cost)
            elif cost_so_far[cur] + 7 < best_cost:
                best_cost = cost_so_far[cur] + 7
                print("found with costs ", best_cost)

        if cost_so_far[cur] + day22.target.manhattan_distance(cur.point) > best_cost:
            continue

        for next_p in get_neighbors(cur.point):
            change, new_tools = change_tool(day22.ground(next_p), day22.ground(cur.point), cur.tool)
            # print(next_p,change)
            if change:
                for n_tool in new_tools:
                    new_cost = cost_so_far[cur] + 1 + 7
                    new_el = Element(n_tool, next_p, cur.priority)
                    if new_el not in cost_so_far or new_cost < cost_so_far[new_el]:
                        cost_so_far[new_el] = new_cost
                        new_el.priority = new_cost + int(day22.target.manhattan_distance(next_p) * 1.3)
                        p_queue.put(new_el)
            else:
                new_cost = cost_so_far[cur] + 1
                new_el = Element(cur.tool, next_p, cur.priority)
                if new_el not in cost_so_far or new_cost < cost_so_far[new_el]:
                    cost_so_far[new_el] = new_cost
                    new_el.priority = new_cost + int(day22.target.manhattan_distance(next_p) * 1.3)
                    p_queue.put(new_el)
        i += 1
    print(best_cost)


if __name__ == "__main__":
    #main()
    cProfile.run('main()')
