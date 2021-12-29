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


def part1(reg, ip, program):
    i = 0
    while reg[ip] < len(program):
        inst = program[reg[ip]]
        tokenz = inst.split()
        if reg[ip] == 28:
            return reg[3]
        globals()[tokenz[0]](*[int(i) for i in tokenz[1:]])
        reg[ip] += 1
        i+=1
    return None


def part2(reg, ip, program):
    for i in range(6):
        reg[i] = 0
    last = None
    possible_vals = set()
    while reg[ip] < len(program):
        inst = program[reg[ip]]
        tokenz = inst.split()
        globals()[tokenz[0]](*[int(i) for i in tokenz[1:]])
        reg[ip] += 1
       # print(reg[ip], inst, reg)
        if reg[ip] == len(program)-1:
            print(reg[3])
            if reg[3] in possible_vals:
                return last
            possible_vals.add(reg[3])
            last = reg[3]
    return None


raw_input = open('../inputs/input_21.txt').read().splitlines()
ip = int(raw_input[0].split()[-1])
program = raw_input[1:]
reg = {i: 0 for i in range(6)}
print("Part 1:",part1(reg, ip, program))


#reg = {i: 0 for i in range(6)}

#print("Part 2:", execute_program(reg, ip, program))
raw_input = open('../inputs/input_21_2.txt').read().splitlines()
ip = int(raw_input[0].split()[-1])
program = raw_input[1:]
print("Part 2:",part2(reg,ip, program))
