import random


while(True):
    inp = input(">> ")
    values = inp.split('d')
    quantity = int(values[0]) if values[0] else 1
    faces = int(values[1])

    pool = []
    for _ in range(quantity):
        pool.append(random.randint(1, faces))

    print('{}\ttotal: {}'.format(sorted(pool), sum(pool)))
