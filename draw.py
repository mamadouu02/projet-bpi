#!/usr/bin/env python3

"""Génération d'une image animée représentant une simulation."""

import subprocess
import sys
import approximate_pi

def pixel_index(x, y, imagesize):
    """Renvoie l'index d'un pixel."""
    return imagesize * (imagesize - 1 - y) + x

def point_to_color(points, colors, imagesize):
    """Convertit les points en couleurs RGB."""
    for point in points:
        x = int((point.x + 1) * (imagesize - 1) // 2)
        y = int((point.y + 1) * (imagesize - 1) // 2)
        index = pixel_index(x, y, imagesize)
        if point.in_circle:
            colors[index] = "0 0 1"
        else:
            colors[index] = "1 0 1"

def digits_to_index(digitsindex, digit, width, height, linewidth, xmin, ymin, imagesize):
    """Ajoute la liste des index des pixels utilisés pour l'affichage des chiffres."""
    vlinewidth = (height - 3 * linewidth) // 2
    if digit == ".":
        digitsindex += [
            pixel_index(x, y, imagesize)
            for x in range(xmin, xmin + width)
            for y in range(ymin, ymin + width)
            ]
    else:
        if digit not in ("1", "4", "7"):
            digitsindex += [
                pixel_index(x, y, imagesize)
                for x in range(xmin + linewidth, xmin + width - linewidth)
                for y in range(ymin, ymin + linewidth)
                ]
        if digit in ("0", "2", "6", "8"):
            digitsindex += [
                pixel_index(x, y + linewidth, imagesize)
                for x in range(xmin, xmin + linewidth)
                for y in range(ymin, ymin + vlinewidth)
                ]
        if digit != "2":
            digitsindex += [
                pixel_index(x + width, y + linewidth, imagesize)
                for x in range(xmin - linewidth, xmin)
                for y in range(ymin, ymin + vlinewidth)
                ]
        if digit not in ("0", "1", "7"):
            digitsindex += [
                pixel_index(x, y + linewidth + vlinewidth, imagesize)
                for x in range(xmin + linewidth, xmin + width - linewidth)
                for y in range(ymin, ymin + linewidth)
                ]
        if digit not in ("1", "2", "3", "7"):
            digitsindex += [
                pixel_index(x, y, imagesize)
                for x in range(xmin, xmin + linewidth)
                for y in range(ymin + 2 * linewidth + vlinewidth, ymin + height - linewidth)
                ]
        if digit not in ("5", "6"):
            digitsindex += [
                pixel_index(x + width, y, imagesize)
                for x in range(xmin - linewidth, xmin)
                for y in range(ymin + 2 * linewidth + vlinewidth, ymin + height - linewidth)
                ]
        if digit not in ("1", "4"):
            digitsindex += [
                pixel_index(x, y, imagesize)
                for x in range(xmin + linewidth, xmin + width - linewidth)
                for y in range(ymin + height - linewidth, ymin + height)
                ]

def memory_to_color(memory, colors):
    """Convertit les pixels stockés en mémoire en couleurs RGB."""
    for elem in memory:
        index, color = elem
        colors[index] = color

def digit_to_color(memory, colors, digitsindex):
    """Convertit les pixels utilisés pour l'affichage des chiffres en couleurs RGB."""
    for index in digitsindex:
        memory.append((index, colors[index]))
        colors[index] = "0 0 0"

def generate_ppm_file(imagesize, colors, filename):
    """Génère une image PPM."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("P3")
        file.write(f"{imagesize} {imagesize}")
        file.write("1")
        for color in colors:
            file.write(color)

def main():
    """Génère une image animée."""

    if len(sys.argv) != 4:
        sys.exit(f"usage: {sys.argv[0]} image_size n_points n_digits")

    image_size = int(sys.argv[1])
    n_points = int(sys.argv[2])
    n_digits = int(sys.argv[3])

    if image_size < 100:
        raise ValueError("image_size must be an integer greater than 100")
    if n_points < 100:
        raise ValueError("n_points must be an integer greater than 100")
    if n_digits < 1 or n_digits > 5:
        raise ValueError("n_digits must be an integer between 1 and 5")

    step = n_points//10
    spacing = image_size * 1//100 + 1
    digit_width = ((image_size * 1//3) + 20) // (n_digits + 1)
    line_width = image_size * 4//1000 + 1
    point_size = image_size * 4//1000 + 2
    display_width = (n_digits + 1) * (spacing + digit_width) + point_size
    display_height = image_size * 15//100 + 5
    y_min = (image_size - display_height) // 2
    
    values, points = approximate_pi.simulation(n_points)
    colors = ["1 1 1" for _ in range(image_size ** 2)]
    memory = []

    for state in range(10):
        value = values[state]
        digits = f"{value:.{n_digits}f}"
        filename = f"img{state}_{digits.replace('.', '-')}.ppm"

        memory_to_color(memory, colors)
        memory = []

        point_to_color(points[step * state:step * (state + 1)], colors, image_size)

        x_min = (image_size - display_width) // 2
        digits_index = []
        for digit in digits:
            width = digit_width
            if digit == ".":
                width = point_size
            digits_to_index(digits_index, digit, width, display_height, line_width,
            x_min, y_min, image_size)
            x_min += width + spacing

        digit_to_color(memory, colors, digits_index)

        generate_ppm_file(image_size, colors, filename)

    subprocess.run("convert -delay 100 -loop 0 img*.ppm img.gif", shell=True, check=False)

if __name__ == "__main__":
    main()
