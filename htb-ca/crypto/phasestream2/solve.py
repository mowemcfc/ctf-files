#!/usr/bin/env python3

from pwn import xor
import re


def solve(ct):
    flag_re = re.compile(b'(CHTB\{.{,60}\})')
    for i in range (1,256):
        key = bytes(chr(i), "utf-8")
        xored = xor(ct, key)

        match = flag_re.search(xored)

        if match:
            print(f"MATCH! key: {key} flag: {match.group(1)}")
            exit()



ct = bytes.fromhex((open("output.txt", "r").read()))
solve(ct)
