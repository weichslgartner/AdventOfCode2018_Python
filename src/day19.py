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


def get_all_numbers(line):
    numbers = re.findall('(\d+)', line)
    return [int(n) for n in numbers]


reg = {i: 0 for i in range(6)}
funcs = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

raw_input = open('../inputs/input_19.txt').read().splitlines()
ip = int(raw_input[0].split()[-1])
program = raw_input[1:]

while reg[ip] < len(program):
    inst = program[reg[ip]]
    # print(inst, reg)
    tokenz = inst.split()
    globals()[tokenz[0]](*[int(i) for i in tokenz[1:]])
    reg[ip] += 1

print("Part1 ",reg[0])
