import base64

from Crypto.Cipher import AES

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA

from config import RSA_PRIVATE_DIR


def  args_decrypted(key,encrypted_text):

    def add_to_16(text):
        while len(text) % 16 != 0:
            text += '\0'
        return str.encode(text)  # 返回bytes

        aes = AES.new(add_to_16(key), AES.MODE_ECB)
        return str(aes.decrypt(base64.decodebytes(bytes(encrypted_text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))


encrypt_text = "JEIQMS21KxarkyKVoqmU60vp0eZzoV8h90NzgnerbrrDMvcUO7XCyVz3kch7iMZV8aiLH7WwA0xFIJxK0J15Ka/Vh8mr7cHhK24z/zOGVgMPXL1TWwWKq76nnsaHlTy4dFcG9iTgJJZtjDZubeigBOundB8uaq5nz8GPOZw2174="
random_generator = Random.new().read

with open(RSA_PRIVATE_DIR) as f:
    key = f.read()
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    text = cipher.decrypt(base64.b64decode(encrypt_text), random_generator)