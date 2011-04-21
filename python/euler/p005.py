#!/usr/bin/env python
# -*- coding: utf-8 -*-

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return (a * b) / gcd(a, b)

ans = 1
for i in range(2, 21):
    ans = lcm(ans, i)
print ans
