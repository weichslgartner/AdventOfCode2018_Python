from collections import namedtuple, defaultdict
from sys import maxsize


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.x} {self.y}'


def get_next_point(char: str, p: Point) -> Point:
    if char == 'E':
        next_point = Point(p.x + 1, p.y)
    elif char == 'W':
        next_point = Point(p.x - 1, p.y)
    elif char == 'N':
        next_point = Point(p.x, p.y + 1)
    elif char == 'S':
        next_point = Point(p.x, p.y - 1)
    else:
        raise Exception("Not a Point")
    return next_point


def solve(inp: str) -> (int, int):
    point_map = defaultdict(lambda: maxsize)
    p = Point(0, 0)
    stack = []
    dist = 0
    for c in inp:
        if c in 'NSWE':
            p = get_next_point(c, p)
            dist += 1
            point_map[p] = min(point_map[p], dist)
        elif c == '(':
            stack.append((dist, p))
        elif c == ')':
            dist, p = stack.pop()
        elif c == '|':
            dist, p = stack[-1]
    return max(point_map.values()), len(list(filter(lambda x: x >= 1000, point_map.values())))


if __name__ == '__main__':
    test_input = open('../inputs/input_20.txt').readline().rstrip()
    part1, part2 = solve(test_input)
    print("Part 1:", part1)
    print("Part 2:", part2)
