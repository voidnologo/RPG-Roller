from collections import Counter
import random


custom_commands = {}
TN_MODIFIER = 0


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


def new_cmd(args=None):
    '''
        Create a new macro
           command = name of command
           pool size = number of dice to roll
           rule-of-six = whether to reroll 6s
           offset = value to add to total
        Usage:
           `{name} [tn]`
    '''
    command = input('Command: ')
    size = int(input('Pool size: '))
    rule_of_six = False if input('Use Rule of Six? Y/n: ').upper() == 'N' else True
    o = input('Offset: ')
    offset = int(o) if o else 0
    custom_commands[command] = dict(size=size, rule_of_six=rule_of_six, offset=offset)


def show_custom(args=None):
    '''
        Show custom macros
        Format is {name} | {pool size} | {use rule-of-six} | {offset}
    '''
    w = max(len(i) for i in custom_commands.keys()) if custom_commands.keys() else 0
    for c in custom_commands.keys():
        size = custom_commands[c]['size']
        ros = 'Y' if custom_commands[c]["rule_of_six"] else 'N'
        off = custom_commands[c]['offset']
        print(f'{c:>{w + 3}} > {size:3} | { ros} | {off:+}')


def print_pool(pool, tn=None, quantity=None, offset=None):
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
    width = len(str(counter.most_common(1)[0][1]))
    for value, amount in sorted(counter.items()):
        print(f'{value:>6}: {amount:{width},} {"." * amount}')
    total_string = f'{total}{offset:+}({total+offset:,})' if offset else f'{total:,}'
    target = (f'({tn[0]}>{int(tn[0]) + TN_MODIFIER})' if TN_MODIFIER else f'({tn[0]})') if tn else ''
    successes = count_successes(counter, int(tn[0]))
    successes_string = f'{successes} success{"" if successes == 1 else "es"} for TN{target}' if tn else ''
    if counter.get(1, 0) >= quantity//2:
        print(f'!! GLITCH !! ')
    print(f'{successes_string}')
    print(f'Total: {total_string}\n')


def count_successes(pool, tn):
    s = 0
    for i in pool:
        if i >= tn + TN_MODIFIER:
            s += pool[i]
    return s


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


def set_tn_modifier(mod=None):
    '''
        Set modifier to Target Numbers
        `:mod` will set it to 0
        `:mod #` will set it to #
        `:mod ?` will display the current value
    '''
    global TN_MODIFIER
    if mod and mod[0] == '?':
        print(f'TN Modifier is: +{TN_MODIFIER}\n')
        return
    TN_MODIFIER = int(mod[0]) if mod else 0
    print(f'TN Modifier is: +{TN_MODIFIER}\n')


def help(args=None):
    for opt in options:
        if options[opt] is not help:
            print(f'{opt} {options[opt].__doc__}')


options = {
    ':n': new_cmd,
    ':l': show_custom,
    ':mod': set_tn_modifier,
    ':help': help,
    ':?': help
}


while(True):
    inp = input(">> ")
    cmd, *args = inp.split()
    if cmd in options.keys():
        options[cmd](args)
        continue
    if cmd in custom_commands.keys():
        quantity = custom_commands[cmd]['size']
        pool = roll_pool(quantity, custom_commands[cmd]['rule_of_six'])
        print_pool(pool, args, quantity=quantity, offset=custom_commands[cmd]['offset'])
        continue
    try:
        quantity = int(cmd)
        pool = roll_pool(quantity)
        print_pool(pool, args, quantity=quantity)
    except Exception as e:
        print('Error:', e)
