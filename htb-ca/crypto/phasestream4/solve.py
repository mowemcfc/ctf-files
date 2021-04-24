#!/usr/bin/env python3

def bytewiseXor(m1,m2):   #taking xor of two messages till the length of smaller message
        xorlen=min(len(m1),len(m2))
        return bytes([m1[i]^m2[i] for i in range(xorlen)])

with open('output.txt', 'r') as f2:
    encrypted = f2.read().split('\n')[0:2]
    ct1 = bytes.fromhex(encrypted[0])
    ct2 = bytes.fromhex(encrypted[1])

crib = b"CHTB{" # it might be helpful to start googling for famous quotes once part of the plaintext is revealed
part_key = bytewiseXor(ct2,crib) 
part_pt1 = bytewiseXor(part_key,ct1)
print(part_pt1)
while True:
    guess = bytes(input("Guess plaintext: "), 'utf8')

    part_key = bytewiseXor(part_pt1 + guess, ct1)
    part_pt1 = bytewiseXor(part_key, ct1)
    part_flag = bytewiseXor(part_key, ct2)
    print(f"plaintext: {part_pt1} flag: {part_flag}")
