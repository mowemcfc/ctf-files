#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import bytes_to_long, long_to_bytes

values = {}

def gen_values(p):
    p.sendline('1')
    p.recvline()
    p.recvline()
    guide = re.findall(b'(\S+?) -> (\d{1,5})', p.recvline())
    for emoji, val in guide:
        values[emoji] = int(val.decode()) 
    p.recvuntil('> ')

def solve():
    p = remote('139.59.185.150',31531)
    p.recvuntil('!\n')
    gen_values(p)
    p.sendline('2')
    p.recvuntil('fast!')
    p.recvuntil('Question 1:\n')
    for i in range(500):
        question = p.recvuntil('?\n').strip(b'\n')
        operators = re.findall(b' *([\*\+\-\=]) *', question)[:-1]
        numbers = re.split(b' \* | \+ | \- |  \= ', question)[:-1]
        numbers = [values[num] for num in numbers]
        result = operation(operators, numbers)
        print(result)
        p.sendline(str(result))
        p.recvline()
        p.recvline()
        print(p.recvline())
        print(p.recvline())
        print(p.recvline())
    print(p.recvline())
    print(p.recvline())
    print(p.recvline())
    return

def operation(ops, nums):
    indices = [i for i, x in enumerate(ops) if x == b"*"]
    while indices:
        indice = indices.pop()
        val = nums[indice] * nums[indice+1]
        del nums[indice]
        del nums[indice]
        del ops[indice]
        nums.insert(indice, val)
        indices = [i for i, x in enumerate(ops) if x == b"*"]
            
    total = nums[0]
    for i, op in enumerate(ops):
        if op == b'+':
            total += nums[i+1]
        else:
            total -= nums[i+1]
    return total

if __name__ == "__main__":
    solve()
