import numpy as np


def get_hundred_digit(number):
    if number < 100:
        return 0
    numb_Str = str(number)
    return int(numb_Str[-3])


def calc_power_level(x, y, serial):
    id = x + 10
    power_level = id * y
    power_level += serial
    power_level *= id
    power_level = get_hundred_digit(power_level)
    power_level -= 5
    return power_level


serial = 9435
grid = np.zeros((301, 301), dtype=int)
grid_sum = np.zeros((301, 301), dtype=int)
grid_sum_mult = np.zeros((301, 301, 301), dtype=int)

for x in range(301):
    for y in range(301):
        grid[y, x] = calc_power_level(x, y, serial)

for x in range(1, 298):
    for y in range(1, 298):
        grid_sum[y, x] = grid[y:y + 3, x:x + 3].sum()

coords = np.unravel_index(grid_sum.argmax(), grid_sum.shape)
print(coords[1], coords[0])

for size in range(1, 300):
    for x in range(1, 300 - size):
        for y in range(1, 300 - size):
            grid_sum_mult[y, x, size] = grid[y:y + size, x:x + size].sum()

coords = np.unravel_index(grid_sum_mult.argmax(), grid_sum_mult.shape)
print(coords[1], coords[0], coords[2])
