#!/usr/bin/env python3

from math import gcd
from Crypto.Util.number import long_to_bytes, inverse
from random import randint
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = egcd(b % a, a)
        return gcd, y - (b // a) * x, x

pub = int(input("enter pub key:"))  
p = 2**1024 + 1657867
MASK = (2**p.bit_length() - 1)
g = 3

priv = inverse(pub, p-1)
priv = 177633458473956537190546041242626112728971204442544418773108803160494994642324572311277331535247516632682529025054221103032200126070890154854126487180148838988445992136922053332004659171365599871916431056653865110912582632782312122859855149866473768769767531729971931974620235550791989177236772979624174702033
assert (pub * priv) % p == 1
print(priv)
print(gcd(pub,priv))

def sign(message: str, x: int):
    while True:
        m = int(message, 16) & MASK
        k = randint(2, p-2)
        if gcd(k, p - 1) != 1:
            continue 
        r = pow(g, k, p)
        s = (m - x*r) * pow(k,-1,p-1) % (p - 1)
        if s == 0:
            continue
        return (r,s)        

def verify(message: str, r: int, s: int, y: int):
    m = int(message, 16) & MASK
    if any([x <= 0 or x >= p-1 for x in [m,r,s]]):
        return False
    return pow(g, m, p) == (pow(y, r, p) * pow(r, s, p)) % p


message = bytes('get_flag','utf8').hex()
r, s = sign(message, priv)
print(r, s)

print(verify(message, r, s, pub))
