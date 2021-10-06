#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.update(arch='i386')

host = args.HOST or 'tartaglia.ctf.fifthdoma.in'
port = int(args.PORT or 14004)


def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)


p = start()
p.recvuntil(b"server")
p.sendline(b"start")

while(1):
    p.recvuntil(b"N:")
    n = int(p.recv(3).strip(),10)
    print(n)

    mul = 1
    sum = 1
    num = 1
    for i in range(0,n-1):
        num = num * 2 
        sum += num

    p.sendline(str(sum))

p.interactive()

