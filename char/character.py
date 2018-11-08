from collections import ChainMap
from dataclasses import dataclass
import random
import json
import sys


@dataclass
class Stat:
    base: int = 0
    ros: bool = True
    offset: int = 0

    def __post_init__(self):
        self.base = int(self.base) if self.base.isdigit() else 0
        self.ros = False if self.ros == 'F' else True
        self.offset = int(self.offset) if self.offset.isdigit() else 0

    def __repr__(self):
        return f'{self.base};{"T" if self.ros else "F"};{self.offset}'


def read_character(file_name):
    with open(file_name) as f:
        return json.load(f)


def lookup_stat(stat):
    raw = ChainMap(stats['attributes'], stats['skills'], stats['pools']).get(stat, ";;")
    return Stat(*(raw.split(';')))


def roll(number, ros=True):
    for _ in range(number):
        die = random.randint(1, 6)
        if ros and die == 6:
            die += next(roll(1))
        yield die


def roll_stat(query):
    try:
        stat = lookup_stat(query)
        if stat.offset:
            yield sum(roll(stat.base, ros=stat.ros)) + stat.offset
        else:
            yield from roll(stat.base, ros=stat.ros)
    except NameError as e:
        print('Failed !!', e)
        return (_ for _ in [])


if __name__ == '__main__':
    file_name = sys.argv[1]
    print(f'Reading character file {file_name}')
    stats = read_character(file_name)
    while True:
        cmd = input('>> ')
        print(list(roll_stat(cmd)))
