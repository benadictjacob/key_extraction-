from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

# Read password from file
password = ''
with open('view.txt', 'r') as f:
    for ch in f:
        password += ch

# Derive key from password
salt = b'\xd0\xacd\xb8@gi\xf4\x17\x87\x171\x9cVd\x06\xeb\\\xacO\x81\xc7\xd3\x04\x0bVV-y\x8b\xcc\x89'
key = PBKDF2(password, salt, dkLen=32)

# Encrypt message
message = b"22.5"
cipher = AES.new(key, AES.MODE_CBC)
ciphered_data = cipher.encrypt(pad(message, AES.block_size))
print("Encrypted:", ciphered_data)

# Write to file (IV + encrypted data)
with open('encrypted.bin', 'wb') as f:
    f.write(cipher.iv)
    f.write(ciphered_data)

# Read from file and decrypt
with open('encrypted.bin', 'rb') as f:
    iv = f.read(16)
    decrypt_data = f.read()

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
original = unpad(cipher.decrypt(decrypt_data), AES.block_size)
print("Decrypted:", original.decode())