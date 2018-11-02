import random


char = {
    'attributes': {
        'strength': 5
    },
    'skills': {
        'pistols': 6
    },
    'pools': {
        'combat': 6
    },
    'meta': {
        'perception': 5,
        'physical_damage': 0,
        'stun_damage': 4
    }
}


def roll(number):
    for _ in range(number):
        die = random.randint(1, 6)
        if die == 6:
            die += next(roll(1))
        yield die


def roll_attribute(attribute):
    number = char['attributes'][attribute]
    return roll(number)


def roll_skill(skill):
    number = char['skills'][skill]
    return roll(number)


def roll_pool(pool):
    number = char['pools'][pool]
    return roll(number)
