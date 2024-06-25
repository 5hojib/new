import os
import string
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from bot import STORE_CHANNEL

BASE62_ALPHABET = string.ascii_letters + string.digits

key = str(STORE_CHANNEL)

def base62_encode(data):
    num = int.from_bytes(data, byteorder='big')
    base62 = ''
    while num > 0:
        num, rem = divmod(num, 62)
        base62 = BASE62_ALPHABET[rem] + base62
    return base62

def base62_decode(data):
    num = 0
    for char in data:
        num = num * 62 + BASE62_ALPHABET.index(char)
    return num.to_bytes((num.bit_length() + 7) // 8, byteorder='big')

def encrypt(text):
    key_bytes = key.encode('utf-8')
    key_bytes = key_bytes[:32].ljust(32, b'\0')
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key_bytes), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = text.encode('utf-8')
    encrypted_bytes = encryptor.update(padded_data) + encryptor.finalize()
    encrypted_data = iv + encrypted_bytes
    encrypted_base62 = base62_encode(encrypted_data)
    return encrypted_base62

def decrypt(encrypted_text):
    key_bytes = key.encode('utf-8')
    key_bytes = key_bytes[:32].ljust(32, b'\0')
    encrypted_data = base62_decode(encrypted_text)
    iv = encrypted_data[:16]  # Extract the 16 bytes IV
    encrypted_bytes = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key_bytes), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_bytes) + decryptor.finalize()
    return decrypted_data.decode('utf-8')
