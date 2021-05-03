# import cProfile
from enum import Enum
from itertools import chain
from typing import List

VERBOSE = False

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
    global_id_cnt = 0

    def __init__(self, units: int, hitpoints: int, initiative: int, weaknesses: List[Damage], immune: List[Damage],
                 attack_type, attack_power: int, army_type: ArmyType, group_id: int):
        self.units = units
        self.hitpoints = hitpoints
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immune = immune
        self.attack_power = attack_power
        self.effective_power = self.units * self.attack_power
        self.attack_type = attack_type
        self.army_type = army_type
        self.group_id = group_id
        self.global_id = Army.global_id_cnt
        Army.global_id_cnt += 1

    def __repr__(self):
        return f"{self.army_type} with ID {self.group_id}  {self.global_id} contains {self.units} units. hitpoints {self.hitpoints}, effective_power {self.effective_power} weak to {self.weaknesses} immune to {self.immune}"

    def damage_received(self, damage: int):
        units_killed = min(damage // self.hitpoints, self.units)
        # print(f"Units killed {units_killed}")
        self.units -= units_killed
        self.effective_power = self.units * self.attack_power

    def damage_dealt_on(self, other):
        if self.attack_type in other.immune:
            return 0
        if self.attack_type in other.weaknesses:
            return self.effective_power * 2
        return self.effective_power


def pos_parenthesis(tokenz: List[str]) -> int:
    i = 7
    if '(' not in tokenz[7]:
        return i
    for token in tokenz[7:]:
        if token.startswith("("):
            tokenz[i] = token[1:]
        elif token.endswith(")"):
            tokenz[i] = token[:-1]
            break
        i += 1
    i += 1
    return i


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
            print(f"parsing error {token}")
    return weaknesses, immune


def parse_input(file_name: str) -> tuple[dict[int, Army], list[Army], list[Army]]:
    armies = {}
    infect_armies = []
    immune_armies = []
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
            line_buffer = line
            #print(line)
            # if is_second_line:
            army = parse_army(army_type, group_id, line_buffer)
            armies[army.global_id] = army
            if army_type == ArmyType.infection:
                infect_armies.append(army)
            else:
                immune_armies.append(army)
            group_id += 1
            #    is_second_line = False
        #  else:
        #     is_second_line = True

    return armies, infect_armies, immune_armies


def parse_army(army_type: ArmyType, group_id: int, line_buffer: str) -> Army:
    tokenz = line_buffer.split()
    #print(tokenz)
    units = int(tokenz[0])
    hitpoints = int(tokenz[4])
    initiative = int(tokenz[-1])
    i = pos_parenthesis(tokenz)
    weaknesses, immune = parse_immune_weaknesses(tokenz[7:i])
    for token in tokenz[i:]:
        i += 1
        if token == 'does':
            break
    attack_power = int(tokenz[i])
    i += 1
    attack_type = Damage(tokenz[i])
    #print(tokenz[7:i + 1])
    return Army(units=units, hitpoints=hitpoints, initiative=initiative, weaknesses=weaknesses, immune=immune,
                army_type=army_type, attack_power=attack_power, attack_type=attack_type, group_id=group_id)




def target_round(attack_army, target_armies, excluded):
    best_target = None
    best_damage = 0

    for im_army in target_armies:
        if im_army.global_id in excluded:
            continue
        damage = attack_army.damage_dealt_on(im_army)
        if damage == 0:
            continue
        if VERBOSE:
            print(
            f"{attack_army.army_type} army {attack_army.group_id} would deal  defending group {im_army.group_id} {damage}")
        if best_target is None:
            best_target = im_army
            best_damage = damage
        if damage >= best_damage:
            if damage > best_damage:
                best_damage = damage
                best_target = im_army
            elif im_army.effective_power > best_target.effective_power:
                best_target = im_army
            elif im_army.effective_power == best_target.effective_power \
                    and im_army.initiative >= best_target.initiative:
                best_target = im_army

    if best_target is not None:
        return best_target.global_id
    return None


def delete_armies(deleted_armies, immune_armies, infect_armies):
    infect_armies = [army for army in infect_armies if army.global_id not in deleted_armies]
    immune_armies = [army for army in immune_armies if army.global_id not in deleted_armies]
    return immune_armies, infect_armies


def sort_armies(immune_armies, infect_armies):
    infect_armies.sort(key=lambda x: (x.effective_power, x.initiative), reverse=True)
    immune_armies.sort(key=lambda x: (x.effective_power, x.initiative), reverse=True)


def attack(armies, target_dict):
    deleted_armies = set()
    for army in sorted(armies.values(), key=lambda x: x.initiative, reverse=True):
        if army.global_id not in target_dict:
            continue
        victim_id = target_dict[army.global_id]
        if VERBOSE:
            print(f"{army.army_type} {army.group_id} attacks {armies[victim_id].group_id}")
        if victim_id in armies:
            damage = army.damage_dealt_on(armies[victim_id])
            if VERBOSE:
                print(f"{army.global_id-1}->{victim_id-1}")

            armies[victim_id].damage_received(damage)
            if armies[victim_id].units <= 0:
                # del armies[victim_id]
                deleted_armies.add(victim_id)
    return deleted_armies


def target_selection(armies, immune_armies, infect_armies):
    target_dict = {}
    for army in infect_armies:
        attack = target_round(army, immune_armies, target_dict.values())
        if attack is not None:
            #print(f"target is {armies[attack].group_id}")
            target_dict[army.global_id] = attack
    for army in immune_armies:
        attack = target_round(army, infect_armies, target_dict.values())
        if attack is not None:
            target_dict[army.global_id] = attack
    return target_dict


def test():
    army = parse_army(ArmyType.immune_system, 1, """1945 units each with 3360 hit points (immune to cold; weak to radiation) with an attack that does 16 cold damage at initiative 1
""")
    assert (army.immune[0] == Damage.cold)
    assert (army.weaknesses[0] == Damage.radiation)

def main():
    test()
    armies: dict[Army]
    infect_armies: List[Army]
    immune_armies: List[Army]
    armies, infect_armies, immune_armies = parse_input("../inputs/input_24.txt")
    i =0
    while len(immune_armies) > 0 and len(infect_armies) > 0:
        sort_armies(immune_armies, infect_armies)
        if VERBOSE:
            print(infect_armies)
            print(immune_armies)
        target_dict = target_selection(armies, immune_armies, infect_armies)
        if VERBOSE:
            print(target_dict)
        deleted_armies = attack(armies, target_dict)

        immune_armies, infect_armies = delete_armies(deleted_armies, immune_armies, infect_armies)
        if VERBOSE:
            print(f"round {i}")
            for a in sorted(infect_armies, key=lambda x: x.units):
                print(a.global_id - 1, a.units)
        i += 1
    #print(immune_armies)
    result = 0
    for army in chain(infect_armies, immune_armies):
        result += army.units
    print("Part 1:", result)  # 15263 14378 too high
    print("Part 2:", 0)


if __name__ == "__main__":
    main()
