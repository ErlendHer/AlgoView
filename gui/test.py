import math


def binary_range(speed, tick):
    base = math.floor(speed)
    step_up = base + 1

    ax = speed - base

    step = 0
    result = []
    prev = 0

    for i in range(tick):
        floored = math.ceil(step)

        result.append(base if floored == prev else step_up)
        prev = floored
        step += ax

    return base, step_up, result

li = binary_range(2, 4)

print(li)
print(len([i for i in li if i == 2]))
