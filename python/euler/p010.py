#!/usr/bin/env python
# -*- coding: utf-8 -*-

maxnum = 2000000
can_div = [True] * (maxnum + 1)

primes = []

for i in range(2, maxnum):
    if can_div[i]:
        primes.append(i)
        for j in range(2, maxnum / i + 1):
            can_div[i * j] = False
print reduce(lambda x, y: x + y, primes)
