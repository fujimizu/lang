#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

for i in range(999, 700, -1):
    for j in range(999, 700, -1):
        val = i * j
        s = str(val)
        is_palindromic = True
        for k in range(len(s) / 2):
            if s[k] != s[-1 - k]:
                is_palindromic = False
                break
        if is_palindromic:
            print i * j, i, j
            sys.exit(0)
