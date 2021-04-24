for line in open("decrypted.txt", 'r'):
    print(bytes.fromhex(line.strip('\n')))
