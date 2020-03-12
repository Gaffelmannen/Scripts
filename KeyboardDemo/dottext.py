#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def text(text_to_print, number_of_dots, number_of_loops):
    import sys
    from time import sleep
    import keyboard
    shell = sys.stdout.shell
    shell.write(text_to_print,'stdout')
    dotes = int(number_of_dots) * '.'
    for last in range(0, number_of_loops):
        for dot in dotes:
            keyboard.write('.')
            sleep(0.15)
        for dot in dotes:
            keyboard.write('\x08')
            sleep(0.15)

if __name__ == "__main__":
    text("Testing", 10, 5)
    print("Hej")

