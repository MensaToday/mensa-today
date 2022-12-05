from base64 import b64decode, b16decode
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.PublicKey import RSA
import os

def decrypt(encrypted_message):
    private_key = os.environ.get('PRIVATE_KEY')
    decode_data = b64decode(encrypted_message)
    if len(decode_data) == 127:
        hex_fixed = '00' + decode_data.hex()
        decode_data = b16decode(hex_fixed.upper())
    imported_private_key = RSA.importKey(b64decode(private_key))
    cipher = Cipher_PKCS1_v1_5.new(imported_private_key)
    decrypted_message = cipher.decrypt(decode_data, None).decode()
    return decrypted_message
