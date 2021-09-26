#!/usr/bin/env python

from base64 import urlsafe_b64decode
from Crypto.Util.number import bytes_to_long, long_to_bytes
from hashlib import sha256
import gmpy2
import requests

link = 'https://web-jwt-b9766b1f.chal-2021.duc.tf/get_token'

jwt0 = requests.get(link).text
jwt1 = requests.get(link).text
#jwt0 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhZG1pbiI6ZmFsc2UsIm5vdyI6MTYzMjU3NzMzMS4xNjU5OTkyfQ.BbrDsXNJ1Roh0muJV0dnMywRvE_KQh75MHJUbmFP61v3IXlaMFBbtwfcZWvheHXq-9UJbgbkQA2zihsISHKerI6pfAsCRFXLbrQNysTAf5x3i84RWr-cZSiI6Qp5EfNERw'
#jwt1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhZG1pbiI6ZmFsc2UsIm5vdyI6MTYzMjU3NzEwMS4xNzQ0Nn0.CzOchPJr7eZkNGtwWOrHuzrnZzr7QzG8iXdlkVHwdUzsFMtS07FlJlETm7r4NQLnWtn7bXQjBG9kc-7y8G3NqJXuvJFGKrSjN9seaMd82OpxPCBrYA4SS19_6yIOEx4qAA'

def pkcs1_v1_5_encode(msg: bytes, n_len: int):
  SHA256_Digest_Info = b'\x30\x31\x30\x0D\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x04\x20'
  T = SHA256_Digest_Info + sha256(msg).digest()
  PS = b'\xFF' * (n_len - len(T) - 3)
  return b'\x00\x01' + PS + b'\x00' + T

def get_magic(jwt):
  header, payload, signature = jwt.split(".")

  raw_signature = urlsafe_b64decode(f"{signature}==")
  raw_signature_int = gmpy2.mpz(bytes_to_long(raw_signature))

  padded_msg = pkcs1_v1_5_encode(f"{header}.{payload}".encode(), len(raw_signature))
  padded_int = gmpy2.mpz(bytes_to_long(padded_msg))

  return gmpy2.mpz(pow(raw_signature_int, e) - padded_int)


e = gmpy2.mpz(65537)

magic0 = get_magic(jwt0)
magic1 = get_magic(jwt1)

print(f'magic0 len({len(str(magic0))})')
print(f'magic1 len({len(str(magic1))})')

N = gmpy2.gcd(magic0, magic1)
assert N != 1
print(hex(N))
