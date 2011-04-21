#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def fib(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return fib(n - 2) + fib(n - 1)

i = 0
sum = 0
while True:
    value = fib(i)
    if value >= 4000000:
        print sum
        sys.exit(0)
    if value % 2 == 0:
        sum += value
    i += 1
