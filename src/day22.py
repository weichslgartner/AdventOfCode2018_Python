import sys
from collections import namedtuple
import cProfile
import dataclasses
from enum import Enum, IntEnum
from typing import Set, List
from queue import PriorityQueue


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.y} {self.x}'

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
    cost: int  = dataclasses.field(compare=False)
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

    def geologic_index(self, p: Point) -> int:
        if p == Point(0, 0) or p == self.target:
            return 0
        elif p.y == 0:
            return p.x * 16807
        elif p.x == 0:
            return p.y * 48271
        return self.erosion_levels[Point(p.x - 1, p.y)] * self.erosion_levels[Point(p.x, p.y - 1)]

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


def change_tool(rtype: RegionType, cur_tool: Tool) -> [bool, List[Tool]]:
    if rtype == RegionType.ROCKY:
        if cur_tool == Tool.TORCH or cur_tool == Tool.CLIMBING_GEAR:
            return False, []
        return True, [Tool.TORCH, Tool.CLIMBING_GEAR]
    if rtype == RegionType.WET:
        if cur_tool == Tool.NEITHER or cur_tool == Tool.CLIMBING_GEAR:
            return False, []
        return True, [Tool.NEITHER, Tool.CLIMBING_GEAR]
    if rtype == RegionType.NARROW:
        if cur_tool == Tool.NEITHER or cur_tool == Tool.TORCH:
            return False, []
        return True, [Tool.NEITHER, Tool.TORCH]


def main():
    day22 = Day22(depth=510, target=Point(10, 10))
    day22 = Day22(depth=7305, target=Point(13, 734))
    print(day22.eval_risk_level)
    p_queue = PriorityQueue()
    p_queue.put(Element(Tool.TORCH, Point(0, 0), 0, day22.target.manhattan_distance(Point(0, 0))))
    best_cost = 1034 #sys.maxsize
    visited = {}
    i = 0
    while not p_queue.empty():
        cur: Element = p_queue.get()
        if i == 10000:
            print(cur.point,cur.cost, cur.priority, cur.tool)
            i=0

        if cur.point == day22.target and cur.cost < best_cost:
            if cur.tool == Tool.TORCH:
                best_cost = cur.cost
            elif cur.cost + 7 < best_cost:
                best_cost = cur.cost + 7
                print("found with costs ", best_cost)
        if cur.cost + day22.target.manhattan_distance(cur.point) >= best_cost:
            continue
        for next_p in get_neighbors(cur.point):
            change, new_tools = change_tool(day22.ground(next_p), cur.tool)
            # print(next_p,change)
            if change:
                for n_tool in new_tools:
                    el = Element(n_tool, next_p, cur.cost + 1 + 7,
                                 day22.target.manhattan_distance(next_p) + cur.cost + 1 + 7)
                    # el.visited.add(cur.point)
                    if el.cost < best_cost and (el not in visited or visited[el] <= el.cost):
                        visited[el] = el.cost
                        p_queue.put(el)
            else:
                el = Element(cur.tool, next_p, cur.cost + 1,
                             day22.target.manhattan_distance(next_p) + cur.cost + 1)
                # el.visited.add(cur.point)
                if el.cost < best_cost and (el not in visited or visited[el] <= el.cost):
                    visited[el] = el.cost
                    p_queue.put(el)
        i += 1
    print(best_cost)


if __name__ == "__main__":
    main()
    #cProfile.run('main()')
