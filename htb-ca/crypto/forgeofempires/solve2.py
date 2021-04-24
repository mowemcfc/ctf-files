from Crypto.Util.number import long_to_bytes, bytes_to_long, GCD
from random import randint

def verify(message: str, r: int, s: int, y: int):
    m = message & MASK
    if any([x <= 0 or x >= p-1 for x in [m,r,s]]):
        return False
    return pow(g, m, p) == (pow(y, r, p) * pow(r, s, p)) % p


p = 2**1024 + 1657867
g = 3
MASK = (2**p.bit_length() - 1)
print(MASK)
y = int(input("enter y: "))


r_list = {}
for e in range(1,p-1):
    r = (g**e * y) % p
    s = (-r) % (p-1)
    m_target = (e*s) % (p-1)
    if r in r_list:
        print("found r collision")
        print("r: {r}")
        print("s1: {r_list[r][0]")
        print("m1: {r_list[r][1]")
        print("s2: {s}")
        print("m2: {m_target}")
        break
    r_list[r] = [s, m_target]
    """
    if verify(m_target, r, s, y):
       print("verified") 
       print(f"r: {r}")
       print(f"s: {s}")
       print(f"m: {m_target}")
       break
    """
