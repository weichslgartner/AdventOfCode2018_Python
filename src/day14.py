def create_recipes(part1: bool, input: str, window: int = 10):
    recipe_list = [3, 7]
    elf1_pos = 0
    elf2_pos = 1

    puzzle_input = int(input)
    len_in = len(input)
    for i in range(1_000_000_000):
        score_1 = recipe_list[elf1_pos]
        score_2 = recipe_list[elf2_pos]
        new_sum = score_1 + score_2
        if new_sum > 9:
            recipe_list.append(1)
            recipe_list.append((new_sum % 10))
        else:
            recipe_list.append(new_sum)

        elf1_pos += 1 + score_1
        elf1_pos %= len(recipe_list)
        elf2_pos += 1 + score_2
        elf2_pos %= len(recipe_list)
        # list can be extended max two new recipes
        chunk = recipe_list[-(len_in + 2):]
        if not part1 and (input in ''.join(map(str, chunk))):
            print('part2: ', str(''.join(map(str, recipe_list)).index(input)))
            break

        if part1 and len(recipe_list) > (puzzle_input + window):
            chunk = recipe_list[puzzle_input:puzzle_input + window]
            result = ''.join(map(str, chunk))
            print('part1: ', result)
            break


if __name__ == '__main__':
    create_recipes(part1=True, input='074501')
    create_recipes(part1=False, input='074501')
