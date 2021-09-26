#!/usr/bin/env python3

from pwn import *
import textwrap 
from json import loads, dumps
import binascii
import string
import time
import random
from base64 import b64encode, b64decode

known_pt = "DUCTF{"
flag = [c for c in known_pt]
blockindex = 2
blocksize = 16
charset = string.ascii_lowercase + string.digits + string.punctuation

HOST = "pwn-2021.duc.tf"
PORT = 31914

p = remote(HOST, PORT)
while flag[:-1] != "}":
    p.recvuntil(b"plaintext:")
    #pt = (b"A"*(blocksize*3-len(flag)-1))
    pt = "".join(flag)
    p.sendline(pt)
    p.recvline()
    r = b64decode(p.recvline().split(b'\n')[0])
    blocks = [r[16*i:16*i+16] for i in range(0,len(r)//16)]
    target = blocks[blockindex]
    for c in charset:
        #pt = bytes("".join(flag) + c + "A"*(blocksize*3-len(flag)-1), 'utf-8')
        rand_choice = "".join(random.choices(charset,k=10))
        pt = bytes("".join(flag) + rand_choice, 'utf-8')
        p.sendline(pt)
        p.recvline()
        r = b64decode(p.recvline().split(b'\n')[0])
        blocks = [r[16*i:16*i+16] for i in range(0,len(r)//16)]
        print(blocks)
        block = blocks[blockindex]
        print(f"TARGET: {target} | CHARS: {rand_choice} | BLOCK: {block} | FLAG: {''.join(flag)}")
        if block == target:
            flag.append(rand_choice)
            break
