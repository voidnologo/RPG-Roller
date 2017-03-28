from collections import Counter
import random


custom_commands = {}


def roll_pool(quantity, rule_of_six=True):
    if rule_of_six:
        return six_roll(quantity)
    return straight_roll(quantity)


def six_roll(quantity):
    for _ in range(quantity):
        die = random.randint(1, 6)
        if die == 6:
            die += next(six_roll(1))
        yield die


def straight_roll(quantity):
    for _ in range(quantity):
        yield random.randint(1, 6)


def new():
    command = input('Command: ')
    size = int(input('Pool size: '))
    rule_of_six = False if input('Use Rule of Six? Y/n: ').upper() == 'N' else True
    custom_commands[command] = dict(size=size, rule_of_six=rule_of_six)


def show_custom():
    for c in custom_commands.keys():
        size = custom_commands[c]['size']
        ros = 'Y' if custom_commands[c]["rule_of_six"] else 'N'
        print(f'{c:>15} > {size:5}\t{ros}')


def print_pool(pool):
    try:
        acc = accumulate()
        next(acc)
        while True:
            acc.send(next(pool))
    except StopIteration:
        try:
            acc.send(None)
        except StopIteration as data:
            counter, total = data.value
    for k in sorted(counter.keys()):
        print(f'{k:6>}: {counter[k]:,}')
    print(f'total: {total:,}')


def accumulate():
    accumulator = Counter()
    total = 0
    while True:
        die = yield
        if die is None:
            break
        total += die
        accumulator.update({die: 1})
    return accumulator, total


options = {
    ':n': new,
    ':l': show_custom,
}


while(True):
    inp = input(">> ")
    try:
        options[inp]()
    except KeyError:
        try:
            quantity = custom_commands[inp]['size']
            pool = roll_pool(quantity, custom_commands[inp]['rule_of_six'])
            print_pool(pool)
        except KeyError:
            try:
                quantity = int(inp)
                pool = roll_pool(quantity)
                print_pool(pool)
            except Exception:
                print('Invalid input')
        except Exception:
            print('Invalid input')
    except Exception:
        print('Invalid input')
