#!/usr/bin/env python3

"""Calcul d'une valeur approximative de pi à l'aide d'une simulation de Monte-Carlo."""

import sys
from random import uniform

class Point:
    
    def __init__(self, x, y, in_circle):
        self.x = x
        self.y = y
        self.in_circle = in_circle

def simulation(n):
    """Génère aléatoirement n points puis renvoie la valeur approximative de pi et la liste des points."""

    count = 0
    values = []
    points = []

    for i in range(1, n+1):
        x = uniform(-1, 1)
        y = uniform(-1, 1)
        in_circle = x**2 + y**2 < 1
        if in_circle:
            count += 1
        
        if __name__ == "__main__":
            continue
        
        if i % (n // 10) == 0:
            values.append(4 * count/i)
        points.append(Point(x, y, in_circle))

    if __name__ == "__main__":
        return 4 * count/n

    return values, points

def main():
    """Calcule une valeur approximative de pi."""

    if len(sys.argv) != 2:
        sys.exit(f"usage: {sys.argv[0]} n_points")
    
    n = int(sys.argv[1])
    pi = simulation(n)
    print(pi)

if __name__ == "__main__":
    main()
    