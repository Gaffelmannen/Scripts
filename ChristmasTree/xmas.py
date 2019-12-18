#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import keyboard
from random import randint
from time import sleep

class ChristmasTree:
    width = 42
    treesize = randint(1, width)
    def draw(self):
        print("\033c")
        for i in range(1, self.width, 2):
            treerow = randint(1, self.treesize)
            if i == 1:
                ch = "$"
            elif treerow % 4 == 0:
                ch = "o"
            elif treerow % 3 == 0:
                ch = "i"
            else:
                ch = "*"
            print("{:^45}".format(ch*i))
        print("{:^45}".format("|||"))
        print("{:^45}".format("|||"))
        sleep(.75)


if __name__ == "__main__":
    xmastree =  ChristmasTree()
    try:
        while True:
            xmastree.draw()
            if keyboard.is_pressed('q'):
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        pass
    sys.exit(0)
