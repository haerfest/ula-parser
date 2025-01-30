#!/usr/bin/env python3

import cv2
import numpy as np
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


class Component:
    radius = 5
    color  = (0, 255, 0, 255)  # BGRA

    def __init__(self, name, point1, point2=None):
        self.name =  name
        self.point1  = point1
        self.point2  = point2

    def draw(self, image, top_left):
        if self.point1: cv2.circle(image, (top_left.x + self.point1.x, top_left.y + self.point1.y), Component.radius, Component.color, -1)
        if self.point2: cv2.circle(image, (top_left.x + self.point2.x, top_left.y + self.point2.y), Component.radius, Component.color, -1)

class Cell:
    width     = 195
    height    = 179
    color     = (0, 0, 255, 255)  # BGRA
    thickness = 2

    def __init__(self, top_left):
        self.top_left = top_left
        self.components = [
            Component('RL1', Point(44, 14), Point(100, 14)),
            Component('Vs1', Point(115, 14)),
            Component('Vs2', Point(172, 28)),
            Component('Rcs', Point(129, 14), Point(185, 14)),
            Component('RL2', Point(129, 14), Point(185, 71)),
            Component('T1B', Point(58, 70)),
            Component('T1E', Point(58, 86)),
            Component('T2E', Point(58, 113)),
            Component('T2B', Point(58, 127)),
            Component('T{1+2}C1', Point(44, 43)),
            Component('T{1+2}C2', Point(15, 99)),
            Component('T{1+2}C3', Point(87, 170)),
            Component('T3B', Point(100, 127)),
            Component('T3E', Point(115, 127)),
            Component('T4E', Point(143, 127)),
            Component('T4B', Point(157, 127)),
            Component('T{3+4}C1', Point(114, 170)),
            Component('T{3+4}C2', Point(186, 99)),
            Component('T5B', Point(128, 57), Point(128, 83)),
            Component('T5E1', Point(108, 60)),
            Component('T5E2', Point(108, 81)),
            Component('T5C', Point(144, 57), Point(144, 83)),
            Component('GND', Point(155, 57), Point(155, 83)),
            Component('X1', Point(15, 14), Point(15, 72)),
            Component('X2', Point(15, 129), Point(59, 170)),
            Component('X3', Point(142, 170), Point(185, 127))
        ]

    def draw(self, image):
        cv2.rectangle(image, (self.top_left.x, self.top_left.y), (self.top_left.x + Cell.width, self.top_left.y + Cell.height), Cell.color, Cell.thickness)
        for component in self.components:
            component.draw(image, self.top_left)

class Ula:
    width                = 10106
    height               = 9194
    top_left_cell        = Point(922, 915)
    gap_vertical         = 32.5
    gap_horizontal       = 17
    group_gap_vertical   = 212
    group_gap_horizontal = 216

    def __init__(self):
        self.cells = []

        y = Ula.top_left_cell.y
        for row_group in range(3):
            for row in range(11):
                x = Ula.top_left_cell.x
                for column_group in range(4):
                    for column in range(9):
                        self.cells.append(Cell(Point(int(x), int(y))))
                        x += Cell.width + Ula.gap_horizontal
                    x += Ula.group_gap_horizontal
                    y -= 2.5  # perspective
                y += Cell.height + Ula.gap_vertical
                y += 2.5 * 4  # perspective
                x += 2
            y += Ula.group_gap_vertical
            x -= 6  # perspective
            y += 2.5  # perspective

    def draw(self, image):
        for cell in self.cells:
            cell.draw(image)
        

def main():
    image = np.zeros((Ula.height, Ula.width, 4), np.uint8)
    ula = Ula()
    ula.draw(image)
    cv2.imwrite('cells.png', image)

if __name__ == '__main__':
    main()
