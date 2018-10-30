import random
from collections import Counter


while(True):
    inp = input(">> ")
    values = inp.split('d')
    quantity = int(values[0]) if values[0] else 1
    sides = int(values[1])

    pool = Counter()
    for _ in range(quantity):
        pool.update({random.randint(1, faces): 1})

    print('{}\ntotal: {:,}'.format(sorted(pool.elements()), sum(pool.elements())))
