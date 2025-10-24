import random

def one_in_x(x: int) -> bool:
    return random.randint(1, x) == 1