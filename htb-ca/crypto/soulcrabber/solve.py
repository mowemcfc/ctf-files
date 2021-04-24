#!/usr/bin/env python3

from Crypto.Util.number import long_to_bytes

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])




ct = long_to_bytes(0x1b591484db962f7782d1410afa4a388f7930067bcef6df546a57d9f873)
seed = long_to_bytes(13371337)
open("out.txt","wb").write(ct)
#solve(ct, seed)

