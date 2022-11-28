#!/usr/bin/env python3

"""Calcul d'une valeur approximative de pi à l'aide d'une simulation de Monte-Carlo."""

from sys import argv
from random import uniform
from collections import namedtuple

Point = namedtuple("Point", "x, y, in_circle")

def generator(n_points):
    """Génère aléatoirement n points et la valeur approximative de pi."""

    count = 0
    for i in range(1, n_points+1):
        x = uniform(-1, 1)
        y = uniform(-1, 1)
        in_circle = x**2 + y**2 < 1
        count += int(in_circle)

        if __name__ == "__main__":
            continue

        yield Point(x, y, in_circle)
        if i % (n_points // 10) == 0:
            yield 4 * count/i

    if __name__ == "__main__":
        yield 4 * count/n_points

def main():
    """Calcule une valeur approximative de pi."""

    if len(argv) != 2:
        raise IndexError(f"usage: {argv[0]} n_points")

    if not argv[1].isdigit():
        raise ValueError("n_points must be an integer")

    n_points = int(argv[1])
    print(next(generator(n_points)))

if __name__ == "__main__":
    main()
