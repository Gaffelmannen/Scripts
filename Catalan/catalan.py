#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def calculate_catalan(n):
    if n <= 1:
        return 1
    result = 0
    for i in range(n):
        result += calculate_catalan(i) * calculate_catalan(n-i-1)
    return result

def verify_number(input):
    try:
       value = int(input)
       return value
    except ValueError:
       return None

iterations = None

while iterations == None:
    value = input("Ange antal iterationer: ")
    iterations = verify_number(value)

for i in range(iterations):
    print(calculate_catalan(i))
