def part1(numbers_array):
    return sum(numbers_array)


def part2(numbers_array):
    seen_frequency = set()
    frequency = 0
    while True:
        for number in numbers_array:
            if frequency in seen_frequency:
                return frequency
            else:
                seen_frequency.add(frequency)
            frequency += number


numbers_array = []
with open('../input/input_1.txt') as f:
    for line in f.readlines():
        numbers_array.append(int(line))

# part 1
print(part1(numbers_array))

# part 2
print(part2([+1, -1]))
print(part2([+3, +3, +4, -2, -4]))
print(part2([-6, +3, +8, +5, -6]))
print(part2(numbers_array))
