from collections import Counter
import random


custom_commands = {}


def roll_pool(quantity, faces, rule_of_six=True):
    if rule_of_six:
        return six_roll(quantity, faces)
    return straight_roll(quantity, faces)


def six_roll(quantity, faces):
    for _ in range(quantity):
        die = random.randint(1, faces)
        if die == 6:
            die += next(six_roll(1, faces))
        yield die


def straight_roll(quantity, faces):
    for _ in range(quantity):
        yield random.randint(1, faces)


def generic(val):
    values = val.split('d')
    quantity = int(values[0]) if values[0] else 1
    faces = int(values[1])
    return quantity, faces


def new():
    command = input('Command: ')
    size = input('Pool size: ')
    number = input('Type of die: ')
    rule_of_six = False if input('Use Rule of Six? Y/n: ').upper() == 'N' else True
    custom_commands[command] = dict(size=size, number=number, rule_of_six=rule_of_six)


def show_custom():
    for c in custom_commands.keys():
        size = custom_commands[c]['size']
        number = custom_commands[c]['number']
        ros = 'Y' if custom_commands[c]["rule_of_six"] else 'N'
        print(f'{c} > {size}d{number}\t{ros}')


def print_pool(pool):
    if len(pool) < 10:
        print(f'{sorted(pool)}')
    else:
        p = Counter(pool)
        for k in sorted(p.keys()):
            print(f'{k:6>}: {p[k]}')
    print(f'total: {sum(pool)}')


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
            quantity, faces = generic(f"{custom_commands[inp]['size']}d{custom_commands[inp]['number']}")
            pool = list(roll_pool(quantity, faces, custom_commands[inp]['rule_of_six']))
            print_pool(pool)
        except KeyError:
            try:
                quantity, faces = generic(inp)
                pool = list(roll_pool(quantity, faces))
                print_pool(pool)
            except Exception:
                print('Invalid input')
        except Exception:
            print(e)
    except Exception:
        print('Invalid input')
