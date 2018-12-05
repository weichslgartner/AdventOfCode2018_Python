import time

from joblib import Parallel, delayed

input = open('../inputs/input_5.txt').read().rstrip()


def replace(in_str) -> str:
    out = ""
    i = 0
    while i < len(in_str):
        if i < (len(in_str)) - 1 and abs(ord(in_str[i]) - ord(in_str[i + 1])) == 32:
            i += 2
        else:
            out += in_str[i]
            i += 1
    return out


def reduce(input):
    while True:
        out = replace(input)
        if len(out) == len(input):
            # print(len(out))
            return len(out)
        else:
            input = out


# part1
print(reduce(input))


def remove_char(char):
    c = chr(char)
    r_input = input
    r_input = r_input.replace(c, '')
    r_input = r_input.replace(c.lower(), '')
    return reduce(r_input)


def part2_seq():
    lengths = []
    for char in range(ord('A'), ord('Z')):
        lengths.append(remove_char(char))
    return lengths


def part2_par():
    return Parallel(n_jobs=-1)(delayed(remove_char)(char) for char in range(ord('A'), ord('Z')))


# part2
# start_time = time.time()
# print('seq',min(part2_seq()),time.time()-start_time)
start_time = time.time()
print('par', min(part2_par()))
print(f'exec_time {time.time() - start_time}')
