from collections import Counter

import numpy as np


def get_adjacent(grid, x, y):
    adjacent = []
    for y_ in range(max(0, y - 1), min(y + 2, len(grid))):
        for x_ in range(max(0, x - 1), min(x + 2, len(grid[y]))):
            if x == x_ and y == y_:
                continue
            adjacent.append(grid[y_][x_])
    return adjacent


def calculate_score(grid, rounds):
    #  global last_results, i, grid, idx, offset
    last_results = []
    new_grid = grid.copy()
    for i in range(rounds):
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                new_cell(grid, new_grid, x, y)
        grid = new_grid.copy()
        # print(grid)
        count = Counter(list(grid.ravel()))
        new_value = count['|'] * count['#']
        last_results.append(new_value)
        # print(i,count['|'], count['#'], count['|'] * count['#'])
        if last_results[-1] in last_results[:-2] and last_results[-5] in last_results[:-5]:
            idx = last_results.index(new_value)
            offset = i - idx
            identical = True
            for j in range(0, 20):
                if last_results[-1 - j] != last_results[idx - j]:
                    identical = False
                    break
            if identical:
                break
    if i == rounds - 1:
        print(last_results[-1])
    else:
        # print(offset, last_results[-offset - 1:-1])
        result_dict = {}
        for i in range(len(last_results) - offset, len(last_results)):
            idx = i % offset
            result_dict[idx] = last_results[i]
        print(result_dict[(rounds - 1) % offset])


def new_cell(grid, new_grid, x, y):
    adjacent = get_adjacent(grid, x, y)
    counter = Counter(adjacent)
    cur = grid[y][x]
    if cur == '.':
        if counter['|'] >= 3:
            new_grid[y][x] = '|'
        else:
            new_grid[y][x] = '.'
    elif cur == '#':
        if counter['|'] >= 1 and counter['#'] >= 1:
            new_grid[y][x] = '#'
        else:
            new_grid[y][x] = '.'
    elif cur == '|':
        if counter['#'] >= 3:
            new_grid[y][x] = '#'
        else:
            new_grid[y][x] = '|'
    else:
        print('undefined symbol')


input = open('../inputs/input_18.txt').read().split('\n')

grid_raw = []

for line in input:
    grid_raw.append(list(line))

grid = np.array(grid_raw)
calculate_score(grid, 10)
grid = np.array(grid_raw)
calculate_score(grid, 1_000_000_000)
