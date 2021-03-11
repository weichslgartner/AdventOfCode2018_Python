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


def initial_fill(points):
    constellations = []
    for p in points:
        found = False
        for c in constellations:
            for p2 in c:
                # print(p,p2,md)
                if p.manhattan_distance(p2) <= 3:
                    c.append(p)
                    found = True
                    #break
            if found:
                break
        if not found:
            constellations.append([p])
    return constellations


def parse_input(file_name: str) -> List[Point]:
    points = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            w, x, y, z = line.split(",")
            points.append(Point(int(w), int(x), int(y), int(z)))
    return points


def solve(points: List[Point]):
    constellations = initial_fill(points)
    print(constellations)
    clusters = [[i] for i in range(len(constellations))]
    for i, c in enumerate(constellations):
        for p in c:
            for j in range(i + 1, len(constellations)):
                for p2 in constellations[j]:
                    if p.manhattan_distance(p2) <= 3:
                        clusters[i].append(j)
    # print(constellations)
    print(clusters)
    unique_sets = set()
    cnt = 0
    for cluster in clusters:
        before_len = len(unique_sets)
        for el in cluster:
            unique_sets.update(clusters[el])
        if len(unique_sets) > before_len:
            cnt += 1
    print(constellations)
    print(cnt)  # 431  too high
    return cnt


if __name__ == "__main__":
    assert solve(parse_input("../inputs/input_25_test.txt")) == 2, "test 0"
    assert solve(parse_input("../inputs/input_25_test1.txt")) == 4, "test 0"
    assert solve(parse_input("../inputs/input_25_test2.txt")) == 3, "test 2"
    assert solve(parse_input("../inputs/input_25_test3.txt")) == 8, "test 3"
