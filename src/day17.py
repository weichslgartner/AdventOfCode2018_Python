import re
import sys
from collections import deque


def calc_water(grid):
    water_rest = 0
    water_drain = 0
    for line in grid:
        for char in line:
            if char in '~':
                water_rest += 1
            elif char == '|':
                water_drain += 1
    return water_rest + water_drain, water_rest


def get_all_numbers(line):
    numbers = re.findall('(\d+)', line)
    return [int(n) for n in numbers]


def parse_grid(file_name='../inputs/input_17.txt'):
    input = open(file_name).read().split('\n')
    min_x = sys.maxsize
    max_x = 0
    min_y = sys.maxsize
    max_y = 0
    coordinates = []
    for line in input:
        tokenz = line.split(',')

        for token in tokenz:
            if 'x' in token:
                x = get_all_numbers(token)
                min_x = min(min_x, min(x))
                max_x = max(max_x, max(x))
            else:
                y = get_all_numbers(token)
                min_y = min(min_y, min(y))
                max_y = max(max_y, max(y))
        coordinates.append((x, y))
    max_x += 2
    min_x -= 2
    max_y += 1
    min_y -= 1
    grid = []
    for y in range(min_y, max_y + 1):
        line = []
        for x in range(min_x, max_x + 1):
            line.append('.')
        grid.append(line)
    max  ###
    # print(grid)
    for coord in coordinates:
        x_range = coord[0]
        y_range = coord[1]
        for y in range(y_range[0], y_range[-1] + 1):
            for x in range(x_range[0], x_range[-1] + 1):
                grid[y - min_y][x - min_x] = '#'

    return min_x, max_x, min_y, max_y, grid


# print_grit(grid)


def print_grit(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            print(grid[y][x], end="")
        print()


def find_walls(line, x_cur):
    next_wall = len(line)
    prev_wall = 0
    for x in range(x_cur, 0, -1):
        if line[x] == '#':
            prev_wall = x
            break
    for x in range(x_cur, max_x - min_x):
        if line[x] == '#':
            next_wall = x
            break
    return prev_wall, next_wall


def flood_line(y, start_x):
    prev_wall, next_wall = find_walls(grid[y], start_x)
    leaked = []
    minx = prev_wall
    maxx = next_wall
    for x in range(start_x, prev_wall, -1):
        minx = x
        if grid[y + 1][x] in '#~':
            if grid[y][x] in '.|':
                grid[y][x] = '~'
        else:
            grid[y][x] = '|'
            leaked.append(x)
            break
    for x in range(start_x, next_wall):
        maxx = x
        if grid[y + 1][x] in '#~':
            if grid[y][x] in '.|':
                grid[y][x] = '~'
        else:
            grid[y][x] = '|'
            leaked.append(x)
            break
    if len(leaked) != 0:
        for x in range(minx, maxx + 1):
            grid[y][x] = '|'
    return leaked


def fill_water_stack(symbol, x, y):
    stack = deque()
    stack.append((symbol, x, y))
    while len(stack) != 0:

        symbol, x, y = stack.pop()
        if y == len(grid) - 1:
            continue
        if symbol == '|':
            grid[y][x] = '|'
            while grid[y + 1][x] == '.' and y + 1 < len(grid) - 1:
                grid[y + 1][x] = '|'
                y += 1
            if grid[y + 1][x] in '~#':
                stack.append(('~', x, y))

        elif symbol == '~' and grid[y][x] != '~':
            grid[y][x] = '~'
            leaked = flood_line(y, x)
            for leak in leaked:
                stack.append(('|', leak, y))
            if (len(leaked) == 0) and (grid[y - 1][x] != '~'):
                stack.append(('~', x, y - 1))


min_x, max_x, min_y, max_y, grid = parse_grid()
print(max_y, len(grid))
grid[0][500 - min_x] = '+'
fill_water_stack('|', 500 - min_x, 1)
print_grit(grid)
print(calc_water(grid))
