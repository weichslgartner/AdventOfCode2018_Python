# import cProfile
from enum import Enum
from typing import List


class ArmyType(str, Enum):
    infection = 'Infection'
    immune_system = 'Immune System'


class Damage(str, Enum):
    fire = 'fire'
    slashing = 'slashing'
    radiation = 'radiation'
    bludgeoning = 'bludgeoning'
    cold = 'cold'


class Army:
    def __init__(self, units: int, hitpoints: int, initiative: int, weaknesses: List[Damage], immune: List[Damage],
                 attack_type, attack_power: int, army_type: ArmyType, group_id: int):
        self.units = units
        self.hitpoints = hitpoints
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immune = immune
        self.attack_power = attack_power
        self.attack_type = attack_type
        self.army_type = army_type
        self.group_id = group_id

    def __repr__(self):
        return f"{self.army_type} with ID {self.group_id} contains {self.units} units. hitpoints {self.hitpoints}"


def parse_immune_weaknesses(tokens: List[str]) -> (List[Damage], List[Damage]):
    weaknesses = []
    immune = []
    is_weak = False
    is_immune = False
    # ['immune', 'to', 'radiation;', 'weak', 'to', 'fire,', 'cold']
    for token in tokens:
        token = token.rstrip(',;')
        if token == 'immune':
            is_immune = True
            is_weak = False
            continue
        elif token == 'weak':
            is_immune = False
            is_weak = True
            continue
        elif token == 'to':
            continue
        if is_weak:
            weaknesses.append(Damage(token))
        elif is_immune:
            immune.append(Damage(token))
        else:
            print("parsing error")
    return weaknesses, immune


def parse_input(file_name: str) -> List[Army]:
    armies = []
    with open(file_name, 'r') as f:
        is_second_line = False
        line_buffer = ""
        army_type = None
        group_id = 1
        # 18 units each with 729 hit points (weak to fire; immune to cold, slashing)
        #  with an attack that does 8 radiation damage at initiative 10
        for line in f.readlines():
            line = line.strip()
            if line == "Immune System:" or line == "Infection:":
                army_type = ArmyType(line.rstrip(':'))
                group_id = 1
                continue
            elif len(line) == 0:
                continue
            if len(line_buffer) != 0:
                line_buffer += ' '
            line_buffer += line
            if is_second_line:
                parse_army(armies, army_type, group_id, line_buffer)
                group_id += 1
                line_buffer = ""
                is_second_line = False
            else:
                is_second_line = True

    return armies


def parse_army(armies, army_type, group_id, line_buffer):
    tokenz = line_buffer.split()
    print(tokenz)
    units = int(tokenz[0])
    hitpoints = int(tokenz[4])
    initiative = int(tokenz[-1])
    i = 7
    for token in tokenz[7:]:
        if token.startswith("("):
            tokenz[i] = token[1:]
        elif token.endswith(")"):
            tokenz[i] = token[:-1]
            break
        i += 1
    i += 1
    weaknesses, immune = parse_immune_weaknesses(tokenz[7:i])
    for token in tokenz[i:]:
        i += 1
        if token == 'does':
            break
    attack_power = int(tokenz[i])
    i += 1
    attack_type = Damage(tokenz[i])
    print(tokenz[7:i + 1])
    armies.append(Army(units=units, hitpoints=hitpoints, initiative=initiative, weaknesses=weaknesses, immune=immune,
                       army_type=army_type, attack_power=attack_power, attack_type=attack_type, group_id=group_id))


def main():
    armies = parse_input("../inputs/input_24.txt")
    print(armies)
    print("Part 1:", 0)
    print("Part 2:", 0)


if __name__ == "__main__":
    main()
