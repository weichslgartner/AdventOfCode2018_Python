from collections import Counter


def compare_ids(id1, id2):
    result = ""
    diff = 0
    for char1, char2 in zip(id1, id2):

        if char1 != char2:
            diff += 1
        else:
            result += char1
        if diff > 1:
            return ""
    return result


def check_id(id):
    exact_two = 0
    exact_three = 0
    count = Counter(id)
    if 2 in count.values():
        exact_two = 1
    if 3 in count.values():
        exact_three = 1
    return exact_two, exact_three


glob_two = 0
glob_three = 0
id_list = []

with open('../input/input_2.txt') as f:
    for id in f.readlines():
        tmp_two, tmp_three = check_id(id)
        glob_two += tmp_two
        glob_three += tmp_three
        for cmp_id in id_list:
            res = compare_ids(cmp_id, id)
            if res != "":
                print(res)
        id_list.append(id)

print(glob_two * glob_three)
