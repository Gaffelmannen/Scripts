#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from time import sleep
from random import randint

prediction = []

while True:
    guess_count = 0
    actual_user_pin = input("Enter PIN: ")[:4]
    calculated_pin = 0

    while actual_user_pin != calculated_pin: 
        guess_count += 1
        prediction.insert(0, randint(0, 9))
        prediction.insert(1, randint(0, 9))
        prediction.insert(2, randint(0, 9))
        prediction.insert(3, randint(0, 9))
        s = [str(i) for i in prediction]
        calculated_pin = str("".join(s))
        prediction = []
    else:
        print("Pin {} was determined in {} iterations.".format( \
            calculated_pin, \
            guess_count)
        )
        print("Do not trust a 4 number code!")
        sys.exit(0)

