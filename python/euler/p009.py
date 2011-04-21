#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sys

for x in range(1, 500):
    for y in range(1, 500):
        z = math.sqrt(x ** 2 + y ** 2)
        if x + y + z == 1000:
            print x * y * z
            sys.exit(0)
