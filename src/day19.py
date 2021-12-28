"""
0 addi 1 16 1
===
1 seti 1 5 5 reg[5] = 1
2 seti 1 2 3 reg[3] = 1
===
3 mulr 5 3 2 reg[2] = reg[5] * reg[3]
4 eqrr 2 4 2 if reg[2] == 10551358:  goto 7: # reg 3 == 5275679 reg[5]==2
5 addr 2 1 1
===
6 addi 1 1 1  --
===
7 addr 5 0 0  reg[0] = reg[0] + reg[5]
8 addi 3 1 3  reg[3] = reg[3] + 1
9 gtrr 3 4 2  if reg[3] > reg[4]:
10 addr 1 2 1    goto 12
===
11 seti 2 6 1 else: goto 3
===
12 addi 5 1 5 reg[5]++
13 gtrr 5 4 2
14 addr 2 1 1
===
15 seti 1 8 1
===
16 mulr 1 1 1
===
17 addi 4 2 4
18 mulr 4 4 4
19 mulr 1 4 4
20 muli 4 11 4
21 addi 2 5 2
22 mulr 2 1 2
23 addi 2 12 2
24 addr 4 2 4
25 addr 1 0 1
===
26 seti 0 4 1
===
27 setr 1 4 2
28 mulr 2 1 2
29 addr 1 2 2
30 mulr 1 2 2
31 muli 2 14 2
32 mulr 2 1 2
33 addr 4 2 4
34 seti 0 3 0
35 seti 0 7 1
===
"""


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


def execute_program(reg, ip, program, patch=False):
    divisors = []
    while reg[ip] < len(program):
        inst = program[reg[ip]]
        tokenz = inst.split()
        if patch and reg[ip] == 4:
            if len(divisors) > 0:
                reg[2] = reg[4]
                reg[5] = divisors.pop(0)
        elif patch and reg[ip] == 9 and reg[5] == reg[4]:
            reg[3] = reg[4] + 1
        elif patch and reg[ip] == 13 and reg[5] == reg[4]:
            reg[5] = reg[4] + 1
        globals()[tokenz[0]](*[int(i) for i in tokenz[1:]])
        if reg[ip] == 33:
            divisors = [1, 2, reg[4] // 2, reg[4]]
        reg[ip] += 1
    return reg[0]


def print_basic_blocks(program):
    for i, inst in enumerate(program):
        print(i, inst)
        if inst[-1] == "1":
            print("===")


raw_input = open('../inputs/input_19.txt').read().splitlines()
ip = int(raw_input[0].split()[-1])
program = raw_input[1:]

reg = {i: 0 for i in range(6)}
print("Part 1:", execute_program(reg, ip, program, False))
reg = {i: 0 for i in range(6)}
reg[0] = 1
print("Part 2:", execute_program(reg, ip, program, True))
