import copy
import queue
import sys
from collections import namedtuple


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.y} {self.x}'


class Player:
    def __init__(self, point, hitpoints=500, attack=3):
        self.point = point
        self.hitpoints = hitpoints
        self.attack = attack


class Elf(Player):
    def __init__(self, point, hitpoints=200, attack=3):
        Player.__init__(self, point, hitpoints=hitpoints, attack=attack)


class Goblin(Player):
    def __init__(self, point, hitpoints=200, attack=3):
        Player.__init__(self, point, hitpoints=hitpoints, attack=attack)


class Node:
    def __init__(self, cost):
        #        self.pred = pred
        self.cost = cost


def print_grid(grid):
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            point = Point(x, y)
            print(char, end="")
        print()


def createDistantMatrix(height, width, defaultNode):
    array = [[copy.deepcopy(defaultNode) for x in range(width)] for i in range(height)]
    return array


def printDistanceMatrix(array):
    for line in array:
        for element in line:
            if element.cost >= 100000:
                print('x', end="\t")
            else:
                print(element.cost, end="\t")
        print()
    print()


def printMaze(array):
    for line in array:
        for char in line:
            print(char, end="")
        print()


def shortestPath(start, destination, maze, distanceMatrix, max_search):
    visited = []
    openSet = queue.PriorityQueue()
    openSet.put((0, start))
    distanceMatrix[start.y][start.x].cost = 0

    while not openSet.empty():
        # printDistanceMatrix(distanceMatrix)
        prio, current = openSet.get(0)
        if current == destination:
            # printDistanceMatrix(distanceMatrix)
            return distanceMatrix[destination.y][destination.x].cost, None

        visited.append(current)
        expandNode(current, openSet, destination, visited, maze, distanceMatrix, max_search)
        # print(destination)
        # printDistanceMatrix(distanceMatrix)
    return None, None


def expandNode(current, openSet, destination, visited, maze, distanceMatrix, max_search):
    for succ in getFreeSuccessors(current, maze, destination):
        if succ in visited:
            continue
        costN = distanceMatrix[current.y][current.x].cost + 1
        if costN > max_search:
            continue

        if any(succ in item for item in openSet.queue) and costN >= distanceMatrix[succ.y][succ.x].cost:
            continue
        # distanceMatrix[succ.y][succ.x].pred = current
        distanceMatrix[succ.y][succ.x].cost = costN
        estimate = costN + manhattanDistance(succ, destination)
        openSet.put((estimate, succ))


def manhattanDistance(current, dest):
    return abs(dest.x - current.x) + abs(dest.y - current.y)


def getFreeSuccessors(current, maze, destination):
    freeSucc = []
    for succ in getSuccessors(current, maze):
        if maze[succ.y][succ.x] == '.' or succ == destination:
            freeSucc.append(succ)
    return freeSucc


def getSuccessors(current, maze):
    succs = []
    if current.y > 0:
        succs.append(Point(current.x, current.y - 1))
    if current.x > 0:
        succs.append(Point(current.x - 1, current.y))
    if current.x < len(maze[0]) - 1:
        succs.append(Point(current.x + 1, current.y))
    if current.y < len(maze) - 1:
        succs.append(Point(current.x, current.y + 1))
    return succs


def should_move(succs, destinations):
    for suc in succs:
        if suc in destinations:
            return False
    return True


def do_fight(destinations: list, is_elf, succs, player):
    """

    :param destinations: list of oppents
    :return:
    """
    fight = False
    min_hitpoints = sys.maxsize
    next_op = None
    backup = []
    killed = None
    for suc in succs:
        if suc in destinations:
            if is_elf:
                op = goblins[suc]
            else:
                op = elves[suc]

            if op.hitpoints <= min_hitpoints:
                backup.append(suc)
            if op.hitpoints < min_hitpoints:
                backup = []
                backup.append(suc)
                min_hitpoints = op.hitpoints
                next_op = op
                if op.point != suc:
                    print('something went wrong')
            fight = True

    if fight:
        backup.sort(key=lambda p: (p.y, p.x))
        if is_elf:
            next_op = goblins[backup[0]]
        else:
            next_op = elves[backup[0]]
        next_op.hitpoints -= player.attack

        if is_elf:
            if next_op.hitpoints < 0:
                grid[next_op.point.y][next_op.point.x] = '.'
                del goblins[next_op.point]
                killed = next_op.point
            else:
                goblins[next_op.point] = next_op
        else:
            if next_op.hitpoints < 0:
                grid[next_op.point.y][next_op.point.x] = '.'
                del elves[next_op.point]
                killed = next_op.point
            else:
                elves[next_op.point] = next_op

    return fight, killed


def parse_raw_input(raw_input, elf_attack_points=3):
    elves = {}
    goblins = {}
    grid = []
    for y, line in enumerate(raw_input):
        line_array = []
        for x, char in enumerate(line):
            if char == 'G':
                goblins[Point(x, y)] = Goblin(Point(x, y))
            elif char == 'E':
                elves[Point(x, y)] = Elf(Point(x, y), attack=elf_attack_points)
            line_array.append(char)
        grid.append(line_array)
    return grid, elves, goblins


def select_next_post(grid, start, destinations):
    defaultNode = Node(100000)
    minCost = sys.maxsize
    next_moves = []
    for succ in getFreeSuccessors(start, grid, (-1, -1)):

        for dest in destinations:
            if manhattanDistance(start, dest) > minCost:
                continue

            distanceMatrix = createDistantMatrix(len(grid), len(grid[0]), defaultNode)
            cost, distanceMatrix = shortestPath(succ, dest, grid, distanceMatrix, minCost)

            if cost == None:
                continue
            # printDistanceMatrix(distanceMatrix)
            if cost <= minCost:

                if cost < minCost:
                    next_moves = []
                    minCost = cost
                next_moves.append((succ, dest))
    if len(next_moves) > 0:
        next_moves = sorted(next_moves, key=lambda p: (p[1].y, p[1].x, p[0].y, p[0].x))
        return next_moves[0][0]
    else:
        return None
        # print(minCost)


def update_grid(grid, move, player_pos):
    grid[move.y][move.x] = grid[player_pos.y][player_pos.x]
    grid[player_pos.y][player_pos.x] = '.'


def update_player_dicts(move, player_pos, player, is_elf):
    if is_elf:
        del elves[player_pos]
        player.point = move
        elves[move] = player
    else:
        del goblins[player_pos]
        player.point = move
        goblins[move] = player


def play_game(grid, elves, goblins, print_verbose=False, part2=True):
    print_grid(grid)
    n_elves = len(elves)
    for i in range(200):
        if print_verbose:
            print('Round ', i)
        killed = []
        keys = list(elves.keys()) + list(goblins.keys())
        for player_pos in sorted(keys, key=lambda p: (p.y, p.x)):
            if player_pos in killed:
                continue
            elif player_pos in elves:
                start = player_pos
                destinations = list(goblins.keys())
                player = elves[player_pos]
                is_elf = True
            elif player_pos in goblins:
                start = player_pos
                destinations = list(elves.keys())
                player = goblins[player_pos]
                is_elf = False
            else:
                # player dead
                continue

            succs = getSuccessors(start, grid)
            if should_move(succs, destinations):
                # see what neighbor has the shortest path to an enemy
                move = select_next_post(grid, start, destinations)
                if move != None:
                    update_grid(grid, move, player_pos)
                    update_player_dicts(move, player_pos, player, is_elf)
                    # we moved, new neighbors
                    succs = getSuccessors(move, grid)

            fight, dead = do_fight(destinations, is_elf, succs, player)
            if n_elves != len(elves) and part2:
                print('Elf died')
                return False
            if dead != None:
                killed.append(dead)
            if len(elves) == 0 or len(goblins) == 0:
                all_val = list(elves.values()) + list(goblins.values())
                hit_sum = sum(player.hitpoints for player in all_val)
                score = i * hit_sum
                print(f'one party is dead after round {i} value: {hit_sum} {i*hit_sum}')
                return True, score

        if print_verbose:
            print_grid(grid)
            for player_pos in sorted(list(elves.keys()) + list(goblins.keys()), key=lambda p: (p.y, p.x)):
                #   comp = oplayers[i]
                #   comp[str(player_pos)]
                # compare_mazes(grid, omazes[i+1])
                if player_pos in elves:
                    print(
                        f'E at {player_pos.x}, {player_pos.y} with hp {elves[player_pos].hitpoints} ')  # { oplayers[i][str(player_pos)]} {elves[player_pos].hitpoints == oplayers[i][str(player_pos)]}')
                elif player_pos in goblins:
                    print(
                        f'G at {player_pos.x}, {player_pos.y} with hp {goblins[player_pos].hitpoints} ')  # { oplayers[i][str(player_pos)]} {goblins[player_pos].hitpoints == oplayers[i][str(player_pos)]}')

    return False


def part2(raw_input):
    for i in range(5, 100):
        print('elf hitpoints', i)
        grid_, elves_, goblins_ = parse_raw_input(raw_input, elf_attack_points=i)
        elves_win, score = play_game(grid_, elves_, goblins_, part2=True)
        if elves_win:
            return score


raw_input = open('../inputs/input_15.txt').read().split('\n')

grid, elves, goblins = parse_raw_input(raw_input)
_, score = play_game(grid, elves, goblins, part2=False)
print('part1', score)
print('part2', part2(raw_input))
