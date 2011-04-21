#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sys

def is_prime(n):
    for i in xrange(2, int(math.sqrt(n))):
        if n % i == 0:
            return False
    return True

num = 600851475143
for i in range(int(math.sqrt(num)), 2, -1):
    if is_prime(i) and num % i == 0:
        print i
        sys.exit(0)
