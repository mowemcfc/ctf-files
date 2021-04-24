#!/usr/bin/env python3

def bytewiseXor(m1,m2):   #taking xor of two messages till the length of smaller message
	xorlen=min(len(m1),len(m2))
	return bytes([m1[i]^m2[i] for i in range(xorlen)])

test = b"No right of private conversation was enumerated in the Constitution. I don't suppose it occurred to anyone at the time that it could be prevented."

with open('output.txt', 'r') as f2:
    encrypted = f2.read().split('\n')
    ct1 = bytes.fromhex(encrypted[0])
    ct2 = bytes.fromhex(encrypted[1])

xored = bytewiseXor(ct1,bytes(test)) 
print(bytewiseXor(xored,ct2))

