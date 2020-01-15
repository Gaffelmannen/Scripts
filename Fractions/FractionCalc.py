#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from fractions import Fraction

class FractionCalc:
    def __init__(self):
        self.lol = 40
        self.lf = "-"

    def calc(self):
        while True:
            try:
                print("\033c")

                a,b = input("Enter first fraction [Format a / b] e.g. 1 2 for 1/2: ").split()
                print(str.format("{}/{}", a, b))
        
                c,d = input("Enter second fraction [Format c / d] e.g. 3 4 for 3/4: ").split()
                print(str.format("{}/{}", c, d))
        
                print(self.lol * self.lf)
                print(str.format("Calculating {}/{} + {}/{} ", a, b, c, d))
                print(self.lol * self.lf)

                a = int(a)
                b = int(b)
                c = int(c)
                d = int(d)

                e = Fraction(a,b) + Fraction(c,d)
                e = str(e)
                print(e)

                print(self.lol * self.lf)
                print(e)

                if len(e) < 3:
                    q = input(str.format("{}Another? [ Y / n ] ", os.linesep))
                else:
                    e = e.split("/")
                    f = int(e[0])
                    g = int(e[1])
                    print("or",round(f/g,2))
                    q = input(str.format("{}Antoher? [ Y / n ] ", os.linesep))
                if q == "n":
                    break
            except:
                pass


if __name__ == "__main__":
    fc = FractionCalc()
    fc.calc()
    print("We are done here")
    sys.exit(0)
