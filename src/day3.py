import re
from collections import namedtuple
from typing import Type, List, Set, Optional

# type definitions
Point = namedtuple('Point', ['x', 'y'])  # type: Type[Point]
Rectangular = namedtuple('Rectangular', ['id', 'x_min', 'y_min', 'x_max', 'y_max'])  # type: Type[Rectangular]


def is_point_in_rectangular(point: Point, rectangular: Rectangular) -> bool:
    return rectangular.x_min <= point.x < rectangular.x_max and rectangular.y_min <= point.y < rectangular.y_max


def get_points(rect1: Rectangular):
    for x in range(rect1.x_min, rect1.x_max):
        for y in range(rect1.y_min, rect1.y_max):
            yield Point(x, y)


def calc_overlap(rect1: Rectangular, rect2: Rectangular) -> List[Point]:
    points = []
    for x in range(rect1.x_min, rect1.x_max):
        for y in range(rect1.y_min, rect1.y_max):
            cur_point = Point(x, y)
            if is_point_in_rectangular(cur_point, rect2):
                points.append(cur_point)
    return points


def get_rectangulars(filename: str = '../inputs/input_3.txt') -> List[Rectangular]:
    with open(filename) as f:
        lines = f.readlines()
    rects = []
    for line in lines:
        m = re.match("#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line)
        rect_id, x, y, width, height = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(
            m.group(5))
        cur_rect = Rectangular(rect_id, x, y, (x + width), (y + height))
        rects.append(cur_rect)
    return rects


def find_overlap_points(rects: List[Rectangular]) -> Set[Point]:
    rect_points = set()
    overlap_points = set()
    for r in rects:
        points = list(get_points(r))
        overlap = rect_points.intersection(points)
        overlap_points.update(overlap)
        rect_points.update(points)
    return overlap_points


def find_rect_wo_overlap(rects: List[Rectangular], overlap_points: Set[Point]) -> Optional[Rectangular]:
    for r in rects:
        points = list(get_points(r))  # type: List[Point]
        intersect = overlap_points.intersection(points)
        if len(intersect) == 0:
            return r
    return None


if __name__ == '__main__':
    # part1
    all_rects = get_rectangulars(filename='inputs/input_3.txt')
    found_overlap_points = find_overlap_points(all_rects)
    print(f'Part 1: Number of overlapping points {len(found_overlap_points)}')
    # part2
    rect = find_rect_wo_overlap(all_rects, found_overlap_points)
    print(f'Part 2: ID of overlap-free Rect: {rect.id}')
