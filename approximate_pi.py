#!/usr/bin/env python3

"""Calcul d'une valeur approximative de pi à l'aide d'une simulation de Monte-Carlo."""

import sys
from random import uniform
from collections import namedtuple

Point = namedtuple("Point", "x, y, in_circle")

def simulation(n_points):
    """Génère aléatoirement n points et la valeur approximative de pi."""

    count = 0
    values = []
    points = []

    for i in range(1, n_points+1):
        x = uniform(-1, 1)
        y = uniform(-1, 1)
        in_circle = x**2 + y**2 < 1
        if in_circle:
            count += 1
        if __name__ == "__main__":
            continue
        if i % (n_points // 10) == 0:
            values.append(4 * count/i)
        points.append(Point(x, y, in_circle))

    if __name__ == "__main__":
        return 4 * count/n_points

    return values, points

def main():
    """Calcule une valeur approximative de pi."""
    n_points = int(sys.argv[1])
    res = simulation(n_points)
    print(res)

if __name__ == "__main__":
    main()
