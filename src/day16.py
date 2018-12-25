import re


def check_reg_addr(a, b, c):
    return a < 4 and b < 4 and c < 4


def check_im_addr(a, b, c):
    return a < 4 and c < 4


def addr(a, b, c):
    reg[c] = reg[a] + reg[b]


def addi(a, b, c):
    reg[c] = reg[a] + b


def mulr(a, b, c):
    reg[c] = reg[a] * reg[b]


def muli(a, b, c):
    reg[c] = reg[a] * b


def banr(a, b, c):
    reg[c] = reg[a] & reg[b]


def bani(a, b, c):
    reg[c] = reg[a] & b


def borr(a, b, c):
    reg[c] = reg[a] | reg[b]


def bori(a, b, c):
    reg[c] = reg[a] | b


def setr(a, b, c):
    reg[c] = reg[a]


def seti(a, b, c):
    reg[c] = a


def gtir(a, b, c):
    if a > reg[b]:
        reg[c] = 1
    else:
        reg[c] = 0


def gtri(a, b, c):
    if reg[a] > b:
        reg[c] = 1
    else:
        reg[c] = 0


def gtrr(a, b, c):
    if reg[a] > reg[b]:
        reg[c] = 1
    else:
        reg[c] = 0


def eqir(a, b, c):
    if a == reg[b]:
        reg[c] = 1
    else:
        reg[c] = 0


def eqri(a, b, c):
    if reg[a] == b:
        reg[c] = 1
    else:
        reg[c] = 0


def eqrr(a, b, c):
    if reg[a] == reg[b]:
        reg[c] = 1
    else:
        reg[c] = 0


def check_func(before, vals, after):
    global funcs
    n_matches = 0
    matched_funs = []
    for fun in funcs:
        for i in range(4):
            reg[i] = before[i]
        fun(*vals)
        if list(reg.values()) == after:
            # print('match', fun.__name__)
            n_matches += 1
            matched_funs.append(fun.__name__)
    return n_matches, matched_funs


def get_all_numbers(line):
    numbers = re.findall('(\d+)', line)
    return [int(n) for n in numbers]


def part1(input):
    instr = []
    before = []
    three_or_more = 0
    fun_dict = {}

    for line in input.split('\n'):
        numbers = get_all_numbers(line)
        if 'Before' in line:
            before = numbers.copy()
        elif 'After' in line:
            after_vals = numbers.copy()
            matches, matched_funs = check_func(before, instr[1:], after_vals)
            if matches >= 3:
                three_or_more += 1
            if instr[0] in fun_dict:
                op_set = fun_dict[instr[0]]
                l_opset = len(op_set)
                op_set.intersection_update(set(matched_funs))
                fun_dict[instr[0]] = op_set
                assert len(op_set) <= l_opset
            else:
                fun_dict[instr[0]] = set(matched_funs)
        elif len(line) > 0:
            instr = numbers.copy()
    print(three_or_more)
    return fun_dict


def run_test_program(input):
    global line, instr
    for i in range(4):
        reg[i] = 0
    for line in input.split('\n'):
        if len(line) == 0:
            continue
        instr = get_all_numbers(line)
        globals()[list(fun_dict[instr[0]])[0]](*instr[1:])
    print(reg[0])


def determine_op_codes(fun_dict):
    while True:
        to_remove = set()
        found_ops = 0

        for key in sorted(fun_dict, key=lambda x: len(fun_dict[x])):
            if len(fun_dict[key]) == 1:
                to_remove.update(fun_dict[key])
                found_ops += 1

            else:
                fun_dict[key].difference_update(to_remove)
        if found_ops == len(fun_dict):
            break


reg = {}
funcs = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

input_parts = open('../inputs/input_16.txt').read().split('\n\n\n')

fun_dict = part1(input_parts[0])
determine_op_codes(fun_dict)

run_test_program(input_parts[1])
