with open('out.txt', 'r') as f:
    ct = bytes.fromhex(f.read())
    print(ct)

with open('out2.txt', 'wb') as f2:
    f2.write(ct)

