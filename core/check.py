import base64
from Crypto import Random
from Crypto.PublicKey import RSA
from config import RSA_PUBLIC_DIR
from config import RSA_PRIVATE_DIR
# 伪随机数生成器



def check_env():
    pass

def production_rsa_key():
    '''
    生成随机秘钥
    :return:
    '''
    random_generator = Random.new().read
    # rsa算法生成实例
    rsa = RSA.generate(1024, random_generator)
    # master的秘钥对的生成
    private_pem = rsa.exportKey()
    with open(RSA_PRIVATE_DIR, 'wb') as f:
        f.write(private_pem)

    public_pem = rsa.publickey().exportKey()
    with open(RSA_PUBLIC_DIR, 'wb') as f:
        f.write(public_pem)