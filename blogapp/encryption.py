from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# RSA Encryption and Decryption
def rsa_encrypt(content, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_content = cipher_rsa.encrypt(content.encode())
    return base64.b64encode(encrypted_content).decode('utf-8')

def rsa_decrypt(encrypted_content, private_key):
    rsa_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    decrypted_content = cipher_rsa.decrypt(base64.b64decode(encrypted_content.encode()))
    return decrypted_content.decode('utf-8')

# Caesar Cipher Encryption and Decryption
def caesar_encrypt(text, shift=3):
    result = ""
    for char in text:
        if char.isalpha():
            shift_amount = 65 if char.isupper() else 97
            result += chr((ord(char) + shift - shift_amount) % 26 + shift_amount)
        else:
            result += char
    return result

def caesar_decrypt(text, shift=3):
    return caesar_encrypt(text, -shift)