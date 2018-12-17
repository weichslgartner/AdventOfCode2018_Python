from collections import deque

# max length of the deque for checking linear behavior
DEQUE_LEN = 10


def parse_lines(file: str) -> (str, dict):
    initial_state = ''
    replacement_rules = {}
    lines = open(file).readlines()

    for line in lines:
        tokenz = line.rstrip().split()
        if len(tokenz) == 0:
            continue
        if 'initial' in tokenz[0]:
            initial_state = tokenz[-1]
        else:
            replacement_rules[tokenz[0]] = tokenz[-1]

    return initial_state, replacement_rules


def sum_plant_spots(state, offset):
    sum_pos = 0
    sum_pots = 0
    for i, char in enumerate(state):
        if char == '#':
            sum_pos += (i - offset)
            sum_pots += 1
    return sum_pos, sum_pots


def expand_field(current_state, offset, expand_token = '.....'):

    if '#' in current_state[0:len(expand_token)]:
        current_state = expand_token + current_state
        offset += len(expand_token)
    if '#' in current_state[-len(expand_token):-1]:
        current_state = current_state + expand_token
    return current_state, offset


def pot_replace(current_state, iterations, window_size, print_output=False):
    offset = 0
    prev_offset = 0
    n_pots_deque = deque([], maxlen=DEQUE_LEN)
    if print_output:
        print(current_state)

    for i in range(iterations):
        current_state, offset = expand_field(current_state, offset)
        current_state_list = list(current_state)
        new_state = current_state
        new_state_list = current_state_list
        for pos in range(len(current_state) - window_size):
            center = pos + 2
            cur_window = ''.join(new_state[pos:pos + window_size])
            if cur_window in rules:
                new_state_list[center] = rules[cur_window]
            else:
                new_state_list[center] = '.'
        new_state = ''.join(new_state_list)
        if print_output:
            print(new_state)
        current_state = new_state
        sum_pot, n_pots = sum_plant_spots(current_state, offset)
        n_pots_deque.append(n_pots)
        # offset is not increasing and number of pots stays constant over the last 10 iterations
        # pots only shift constant to the right
        # stop the iterations and calculate the linear formular
        if n_pots_deque.count(n_pots) == DEQUE_LEN and (prev_offset == offset):
            break
        prev_offset = offset
    if i < iterations-1:
        print(i)
        coeff = n_pots_deque[-1]
        intercept = sum_pot - (i * coeff)
        result = coeff * (iterations - 1) + intercept
    else:
        result = sum_pot
    print(result)


init_state, rules = parse_lines(file='../inputs/input_12.txt')
# get any key for the window length
window_size = len(next(iter(rules.keys())))
iterations = 20
current_state = init_state
pot_replace(current_state, iterations, window_size)

iterations = 50000000000
current_state = init_state
pot_replace(current_state, iterations, window_size)
