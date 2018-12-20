import re


def compare_other():
    raw = open('../inputs/compare_15.txt').read().split('\n')
    cur_round = 0
    cur_maze = []
    mazes = {}
    players = {}
    cur_player = {}
    for line in raw:
        if len(line) < 1:
            continue
        if 'Round' in line:
            cur_round = int(line.split()[-1])
            if len(cur_maze) > 0:
                mazes[cur_round - 2] = cur_maze.copy()
                players[cur_round - 2] = cur_player.copy()
        elif line.startswith('#'):
            cur_maze.append(line)
        elif line.startswith('G') or line.startswith('E'):
            if '-1' in line:
                continue
            numbers = re.findall('(\d+)', line)
            cur_player[str(Point(numbers[0], numbers[1]))] = int(numbers[2])
    return mazes, players


def compare_mazes(maze1, maze2):
    x = 0
    y = 0
    for line1, line2 in zip(maze1, maze2):
        for char1, char2 in zip(line1, line2):
            if char1 != char2:
                print(f'mismatch {x}{y}')
            x += 1
        y += 1


if __name__ == '__main__':
    mazes, players = compare_other()
    print(players[0][str(Point(18, 2))])
