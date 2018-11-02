from collections import ChainMap
import random
import json
import sys


def read_character(file_name):
    with open(file_name) as f:
        return json.load(f)


def roll(number):
    for _ in range(number):
        die = random.randint(1, 6)
        if die == 6:
            die += next(roll(1))
        yield die


def roll_stat(stat):
    try:
        number = ChainMap(char['attributes'], char['skills'], char['pools']).get(stat, 0)
        yield from roll(number)
    except NameError:
        print('Failed !!')
        return (_ for _ in [])


if __name__ == '__main__':
    file_name = sys.argv[1]
    print(f'Reading character file {file_name}')
    char = read_character(file_name)
    while True:
        cmd = input('>> ')
        print(list(roll_stat(cmd)))
