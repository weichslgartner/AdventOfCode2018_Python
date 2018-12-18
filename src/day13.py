from collections import namedtuple
from enum import Enum


class Direction(Enum):
    left = 0
    straight = 1
    right = 2


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.y} {self.x}'


class Cart():
    def __init__(self, cur_char, point):
        self.cur_char = cur_char
        self.point = point
        self.turns = Direction.left

    def get_nex_direction(self):
        res = self.turns
        next_dir = (self.turns.value + 1) % len(Direction)
        self.turns = Direction(next_dir)
        return res

    def __hash__(self):
        return hash(self.point)

    def __repr__(self):
        return f'{self.cur_char} {self.point} {self.turns}'


def print_grid(grid, carts):
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            point = Point(x, y)
            if point in list(carts.keys()):
                t_char = carts[point].cur_char
            else:
                t_char = char
            print(t_char, end="")
        print()


def parse_input(lines):
    grid = []
    carts = {}
    y = 0
    for line in lines:
        line_list = []
        x = 0
        for char in line:
            line_list.append(char)
            if char in '<>v^':
                point = Point(x, y)
                carts[point] = Cart(char, point)
            x += 1
        while x < max_length:
            line_list.append(' ')
            x += 1
        grid.append(line_list)
        y += 1
    return grid, carts


def clean_grid(grid, lines, max_length):
    for y in range(len(lines)):
        for x in range(max_length):
            if grid[y][x] in '><':
                grid[y][x] = '-'
            elif grid[y][x] in '^v':
                grid[y][x] = '|'


def get_next_dir(cart, dir, new_cart, nex_pos):
    if nex_pos == '+':
        nex_dir = cart.get_nex_direction()
        if nex_dir == Direction.left:
            idx = '^<v>'.index(dir)
            new_cart.cur_char = '^<v>'[(idx + 1) % 4]
        elif nex_dir == Direction.right:
            idx = '^>v<'.index(dir)
            new_cart.cur_char = '^>v<'[(idx + 1) % 4]
        elif nex_dir == Direction.straight:
            pass
    elif nex_pos == '\\':
        if dir == '>':
            new_cart.cur_char = 'v'
        elif dir == '<':
            new_cart.cur_char = '^'
        elif dir == '^':
            new_cart.cur_char = '<'
        elif dir == 'v':
            new_cart.cur_char = '>'
        else:
            print('something went wrong \\', dir)
    elif nex_pos == '/':
        if dir == '<':
            new_cart.cur_char = 'v'
        elif dir == '^':
            new_cart.cur_char = '>'
        elif dir == '>':
            new_cart.cur_char = '^'
        elif dir == 'v':
            new_cart.cur_char = '<'
        else:
            print('something went wrong /')
    elif nex_pos == '-':
        if dir == '<':
            new_cart.cur_char = '<'
        elif dir == '>':
            new_cart.cur_char = '>'
        else:
            print('something went wrong -')
    elif nex_pos == '|':
        if dir == '^':
            new_cart.cur_char = '^'
        elif dir == 'v':
            new_cart.cur_char = 'v'
        else:
            print('something went wrong |')


def get_nex_pos(cart, dir, new_cart):
    if dir == '>':
        nex_pos = grid[cart.point.y][cart.point.x + 1]
        new_cart.point = Point(cart.point.x + 1, cart.point.y)
    elif dir == '<':
        nex_pos = grid[cart.point.y][cart.point.x - 1]
        new_cart.point = Point(cart.point.x - 1, cart.point.y)
    elif dir == '^':
        nex_pos = grid[cart.point.y - 1][cart.point.x]
        new_cart.point = Point(cart.point.x, cart.point.y - 1)
    elif dir == 'v':
        nex_pos = grid[cart.point.y + 1][cart.point.x]
        new_cart.point = Point(cart.point.x, cart.point.y + 1)
    return nex_pos


def run_the_carts(carts, part1=True, mx_iter=1_000_000, print_grids=False):
    ticks = 0
    new_carts = carts
    for _ in range(mx_iter):
        carts = new_carts.copy()
        new_carts = {}
        cart_set = set(carts.keys())
        for cart in sorted(carts.values(), key=lambda x: (x.point.y, x.point.x)):
            new_cart = cart
            if new_cart.point not in cart_set:
                continue
            # remove moving cart
            cart_set.remove(cart.point)
            dir = cart.cur_char

            nex_pos = get_nex_pos(cart, dir, new_cart)

            get_next_dir(cart, dir, new_cart, nex_pos)

            if new_cart.point in cart_set:

                if part1:
                    print(f'first crash {new_cart.point.x},{new_cart.point.y}')
                    return
                else:
                    cart_set.remove(new_cart.point)
            else:
                cart_set.add(new_cart.point)
                new_carts[new_cart.point] = new_cart

        if len(cart_set) == 1 and part1 == False:
            last_point = list(cart_set)[0]
            print(f'last cart {last_point.x},{last_point.y}')
            return
        if print_grids:
            print_grid(grid, new_carts)
    return


lines = open('../inputs/input_13.txt').read().split('\n')
max_length = len(max(lines, key=len))
grid, carts = parse_input(lines)
clean_grid(grid, lines, max_length)
run_the_carts(carts, part1=True)
grid, carts = parse_input(lines)
clean_grid(grid, lines, max_length)
run_the_carts(carts, part1=False)
