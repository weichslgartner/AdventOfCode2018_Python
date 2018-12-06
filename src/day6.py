import sys
import time
from collections import namedtuple
from typing import Set, List, Type
from joblib import Parallel, delayed

Point = namedtuple('Point', ['x', 'y'])  # type: Type[Point]


class Cluster:
    def __init__(self, point: Point):
        self.centroid = point
        self.point_set = set()
        self.infinite = False
        self.point_set.add(point)

    def get_size(self):
        return len(self.point_set)

    def __hash__(self):
        return hash(self.centroid)




def manhattan_distance(point1: Point, point2: Point) -> int:
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)


def is_within_max_region(point1: Point, points: List[Point], max_dist: int) -> int:
    manhattan_sum = 0
    for p in points:
        manhattan_sum += manhattan_distance(p, point1)
        if manhattan_sum >= max_dist:
            return 0
    return 1


def find_nearest_centroid(clusters, point):
    nearest_centroid = []
    min_dist = sys.maxsize
    for cluster in clusters.values():
        dist = manhattan_distance(cluster.centroid, point)
        if dist <= min_dist:
            if dist < min_dist:
                nearest_centroid = []
            min_dist = dist
            nearest_centroid.append(cluster.centroid)

    if len(nearest_centroid) == 1:
        return nearest_centroid[0]
    else:
        return None


def parse_centroids(input):
    points = []
    clusters = {}
    for line in input:
        x, y = line.split(',')
        point = Point(int(x), int(y))
        points.append(point)
        clusters[point] = Cluster(point)
    return points, clusters


def points_to_clusters(points, clusters):
    x_max, x_min, y_max, y_min = get_min_max(points)
    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            point = Point(x, y)
            nearest_c = find_nearest_centroid(clusters, point)
            if nearest_c == None:
                continue
            cluster = clusters[nearest_c]
            cluster.point_set.add(point)
            if x == x_min or x == x_max or y == y_min or y == y_max:
                cluster.infinite = True
            clusters[nearest_c] = cluster

    return clusters


def get_min_max(points):
    x_min = min(points, key=lambda point: point.x).x
    x_max = max(points, key=lambda point: point.x).x
    y_min = min(points, key=lambda point: point.y).y
    y_max = max(points, key=lambda point: point.y).y
    return x_max, x_min, y_max, y_min


def get_biggest_finite_field(clusters):
    biggest_size = 0
    for cluster in clusters.values():
        if (cluster.infinite == False) and (cluster.get_size() > biggest_size):
            biggest_size = cluster.get_size()
        # print(cluster.centroid, cluster.get_size(), cluster.infinite)
    return biggest_size


def find_region_within(points, max_dist):
    x_max, x_min, y_max, y_min = get_min_max(points)
    x_range = range(x_min, x_max)
    y_range = range(y_min, y_max)
    # print(x,y,largest_region_within)
    #    largest_region_within += multiple_manhattan_distance(Point(x, y), points, max_dist)
    region_list = Parallel(n_jobs=-1)(
        delayed(is_within_max_region)(Point(x, y), points, max_dist) for x in x_range for y in y_range)
    return sum(region_list)


input = open('../inputs/input_6.txt').readlines()
points, clusters = parse_centroids(input)
start = time.time()
clusters = points_to_clusters(points, clusters)
b_f_field = get_biggest_finite_field(clusters)
print(f'{b_f_field} ({time.time()-start} sec)')

start = time.time()
largest_region = find_region_within(points, max_dist=10000)
print(f'{largest_region} ({time.time()-start} sec)')
