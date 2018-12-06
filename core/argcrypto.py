import base64
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

import binascii
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from config import RSA_PRIVATE_DIR,RSA_PUBLIC_DIR




def enrsa(message):
    with open(RSA_PUBLIC_DIR,"r") as f:
         key = f.read()
         rsakey = RSA.importKey(key)  # 导入读取到的公钥
         cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象

         # 通过生成的对象加密message明文，注意，在python3中加密的数据必须是bytes类型的数据，不能是str类型的数据
         return  base64.b64encode(cipher.encrypt(message.encode(encoding="utf-8")))


def dersa(cipher_text):
    with open(RSA_PRIVATE_DIR,'r') as f:
        key = f.read()
        rsakey = RSA.importKey(key)  # 导入读取到的私钥
        cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象

        # 将密文解密成明文，返回的是一个bytes类型数据，需要自己转换成str
        return cipher.decrypt(base64.b64decode(cipher_text), "ERROR")

c = "krs4PjfFIvmya2uiUzIR+gyNwqOXFqz8QzxO1Vj5qvnEYfeWoYTDLLYjhqiOhmTVvVc+ux6WezQ+y7H1RnmiE9J91V9otwOMiBFiI+XNPkiN2XJj3RwEjLKdLVSoik8jlD+LPcT29SfbGde5JSTgIQP3Z140TV91d1fNJokWepc="

key = '9UXf31kVlYQkFa0uPOznj41iOlVEQJlfW4RT7U8M774L3J3TigXlBjPlT51dqyvA'

# print(key)
aes = "U2FsdGVkX1/O3k4YLPP6bKPTHFk5Ob8IXVrQJ9SqKZZGg0/OWWsUxsTS3+2pFaaM"
print (base64.b64decode(aes))
def decrypt(key, text):
        cryptor = AES.new(key,AES.MODE_CBC,key)
        plain_text = cryptor.decrypt(base64.b64decode(aes))
        return str(plain_text)

print(decrypt(key,aes))


