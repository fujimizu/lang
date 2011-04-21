#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

primes = []
i = 2
while True:
    is_prime = True
    for p in primes:
        if i % p == 0:
            is_prime = False
            break
    if is_prime:
        primes.append(i)
    i += 1
    if len(primes) == 10001:
        print primes[-1]
        sys.exit(0)
