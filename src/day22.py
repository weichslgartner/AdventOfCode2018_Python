import copy
from collections import namedtuple
import cProfile
from dataclasses import dataclass
from enum import Enum

class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.y} {self.x}'


class Tool(Enum):
    TORCH = 1,
    NEITHER = 2,
    CLIMBING_GEAR = 3


@dataclass()
class Element(object):
    tool: Tool
    cost: int




class Day22:
    def __init__(self, depth: int, target: Point):
        self.depth = depth
        self.target = target
        self.erosion_levels = {}

    def geologic_index(self, p: Point) -> int:
        if p == Point(0, 0) or p == self.target:
            return 0
        elif p.y == 0:
            return p.x * 16807
        elif p.x == 0:
            return p.y * 48271
        return self.erosion_levels[Point(p.x-1,p.y)] * self.erosion_levels[Point(p.x,p.y-1)]

    def erosion_level(self, p: Point) -> int:
        if p not in self.erosion_levels.keys():
            self.erosion_levels[p] = (self.geologic_index(p) + self.depth) % 20183
        return self.erosion_levels[p]

    def ground(self, p: Point):
        return self.erosion_level(p) % 3

    def eval_risk_level(self):
        risk_level = 0
        for y in range(self.target.y + 1):

            for x in range(self.target.x + 1):
                ground = self.ground(Point(x=x, y=y))
                c = '.'
                if ground == 1:
                    c = '='
                elif ground == 2:
                    c = '|'
                #print(c, end="")
                risk_level += ground

            #print()
        return risk_level


def main():
    # day22 = Day22(depth=510,target=Point(10,10))
    day22 = Day22(depth=7305, target=Point(13, 734))


    print(day22.eval_risk_level())


if __name__ == "__main__":
    main()
    # cProfile.run('main()')
