def generator_function(a, b):
    for i in range(3):
        yield a+i, b


def main_func():
    gen = generator_function(2, 3)
    while True:
        a = next(gen, -1)
        if a == -1:
            break
        yield a



gen2 = main_func()

for i in range(4):
    print(next(gen2))
