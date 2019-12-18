#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import string
from tkinter import *
from random import choice

class Keygenerator:
    
    def __init__(self):
        self.UPPER_BOUND = 10

    def generate(self):
        self.keyfield.delete(0, END)
        generated_key = []
        for x in range(self.UPPER_BOUND):
            key = list(string.ascii_letters + string.digits)
            key = choice(key)
            generated_key.append(key)
        "".join(generated_key)
        self.keyfield.insert(INSERT, generated_key)
    
    def showkey(self):
        window = Tk()
        window.title("Keygenerator")
        window.geometry("250x32")
        window.minsize(250, 32)
        window.maxsize(250, 32)

        self.keyfield = Entry(window, width=20)
        self.keyfield.place(x=1, y=1)
        
        generatebutton = Button(window, text="Generate", command=self.generate)
        generatebutton.place(x=170,y=1)

        window.mainloop()

if __name__ == "__main__":
    kg = Keygenerator()
    kg.showkey()
    #sys.exit(0)
