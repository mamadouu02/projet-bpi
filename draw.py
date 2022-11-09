#!/usr/bin/env python3

"""Génération d'une image animée représentant une simulation."""

import sys
import subprocess
import approximate_pi

def generate_ppm_file(size, points, state, res):
    """Génère une image PPM."""

    colors = ["w" for _ in range(size ** 2)]

    for point in points:
        x = int((point.x + 1) * (size - 1) // 2)
        y = int((point.y + 1) * (size - 1) // 2)
        index = size * (size - 1 - y) + x
        if point.in_circle:
            colors[index] = 'b'
        else:
            colors[index] = 'm'

    res = str(res).replace('.', '-')
    filename = f'img{state}_{res}.ppm'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("P3\n")
        file.write(f"{size} {size}\n")
        file.write("1\n")
        for color in colors:
            if color == "w":
                file.write("1 1 1\n")
            elif color == "b":
                file.write("0 0 1\n")
            elif color == "m":
                file.write("1 0 1\n")

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

    for state in range(10):
        res = round(values[state], digits)
        generate_ppm_file(size, points[:n_points//10 * (state + 1)], state, res)

    subprocess.run("convert -delay 100 -loop 0 img*.ppm img.gif", shell=True, check=True)

if __name__ == "__main__":
    main()
