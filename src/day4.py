import re
from collections import namedtuple, Counter
from typing import Any, NamedTuple, List, Dict

from dateutil.parser import parse


class Event(NamedTuple):
    time: Any
    wakes: bool = False
    falls: bool = False
    id: int = -1


class Guard():
    def __init__(self, id : int):
        self.id = id
        self.min_sleeping = 0
        self.sleep_counter = Counter()

    def __hash__(self):
        return self.id

    def add_sleeping(self, begin : int, end : int):
        self.min_sleeping += end - begin
        self.sleep_counter += Counter([i for i in range(begin, end)])

    def get_sleepiest_minute(self):
        return self.sleep_counter.most_common(1)[0][0]

    def get_highest_sleep_freq(self):
        if len(self.sleep_counter) > 0:
            return self.sleep_counter.most_common(1)[0][1]
        else:
            return 0

    def get_id_times_sleep_minute(self):
        return self.get_sleepiest_minute() * self.id


def parse_events(lines : List[str]):
    events = []
    for line in lines:
        m = re.match('\[(.*?)\] (.*)', line)
        date_string = m.group(1)
        info_string = m.group(2)
        date = parse(date_string)
        wakes = False
        falls = False
        id = -1
        if 'wakes' in info_string:
            wakes = True
        elif 'falls' in info_string:
            falls = True
        else:
            m = re.match('Guard #(\d+)', info_string)
            id = int(m.group(1))
        event = Event(date, wakes, falls, id)
        events.append(event)
    return events


def create_guard_dict(events : List[Event]) -> Dict[int,Guard]:
    guards = {}
    cur_id = -1
    asleep = None
    for event in events:
        if event.id != -1:
            cur_id = event.id
            guard = Guard(cur_id)
            if cur_id not in guards:
                guards[cur_id] = guard
        if event.falls:
            asleep = event.time.minute
        if event.wakes:
            cur_guard = guards[cur_id]
            cur_guard.add_sleeping(asleep, event.time.minute)
            guards[cur_id] = cur_guard
    return guards


def get_sleepiest_guard(guard_dict : Dict[int,Guard]):
    return max(guard_dict.values(), key=lambda x: x.min_sleeping)


with open('../inputs/input_4.txt') as f:
    lines = f.readlines()

events = parse_events(lines)
events.sort(key=lambda x: x.time.timestamp())

guards = create_guard_dict(events)

# part 1
sleepies_guard = get_sleepiest_guard(guards)
print(sleepies_guard.get_id_times_sleep_minute())

# part 2
most_same_minute = max(guards.values(), key=lambda x: x.get_highest_sleep_freq())
print(most_same_minute.get_id_times_sleep_minute())
