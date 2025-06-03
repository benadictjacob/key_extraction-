from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
import binascii

# Fixed salt
salt = b'\xd0\xacd\xb8@gi\xf4\x17\x87\x171\x9cVd\x06\xeb\\\xacO\x81\xc7\xd3\x04\x0bVV-y\x8b\xcc\x89'

def data_to_token(message: str, password: str) -> str:
    if not password:
        raise ValueError("Encryption key (password) is empty.")
    
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted = cipher.encrypt(pad(message.encode(), AES.block_size))
    return binascii.hexlify(cipher.iv + encrypted).decode()

def token_to_data(token: str, password: str) -> str:
    encrypted = binascii.unhexlify(token)
    iv = encrypted[:16]
    encrypted_data = encrypted[16:]
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted_data), AES.block_size).decode()
