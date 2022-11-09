#!/usr/bin/env python3

"""Génération d'une image animée représentant une simulation."""

import sys
import subprocess
import approximate_pi

def generate_ppm_file(size, points, colors, filename):
    """Génère une image PPM."""

    for point in points:
        x = int((point.x + 1) * (size - 1) // 2)
        y = int((point.y + 1) * (size - 1) // 2)
        index = size * (size - 1 - y) + x
        if point.in_circle:
            colors[index] = "0 0 1\n"
        else:
            colors[index] = "1 0 1\n"

    with open(filename, 'w', encoding='utf-8') as file:
        file.write("P3\n")
        file.write(f"{size} {size}\n")
        file.write("1\n")
        for color in colors:
            file.write(color)

def main():
    """Génère une image animée."""

    if len(sys.argv) != 4:
        sys.exit(f"usage: {sys.argv[0]} image_size n_points n_digits")

    size = int(sys.argv[1])
    n_points = int(sys.argv[2])
    digits = int(sys.argv[3])

    if size < 100:
        raise ValueError("image_size must be an integer greater than 100")
    if n_points < 100:
        raise ValueError("n_points must be an integer greater than 100")
    if digits < 1 or digits > 5:
        raise ValueError("n_digits must be an integer between 1 and 5")

    values, points = approximate_pi.simulation(n_points)
    colors = ["1 1 1\n" for _ in range(size ** 2)]

    for state in range(10):
        res = values[state]
        step = n_points//10
        filename = f'img{state}_{res:.{digits}f}.ppm'.replace('.', '-', 1)
        generate_ppm_file(size, points[step * state:step * (state + 1)], colors, filename)

    subprocess.run("convert -delay 100 -loop 0 img*.ppm img.gif", shell=True, check=False)

if __name__ == "__main__":
    main()
