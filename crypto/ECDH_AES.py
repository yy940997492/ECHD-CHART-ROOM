'''
Author: CUIT渊
Date: 2023-03-18 23:34:05
LastEditTime: 2023-03-19 10:49:29
FilePath: \multiplayer-chat-room-master\crypto\ECDH_AES.py
'''
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from os import urandom
import pickle
import os
from cryptography.hazmat.primitives import serialization

nonce = urandom(12)


def generate_ecc_key():
    private_key = ec.generate_private_key(ec.SECP384R1())
    public_key = private_key.public_key()
    return private_key, public_key


# public_key是发送方的公钥，private_key是接收方的私钥
def generate_shared_key(private_key, public_key):
    # 假设Bob收到Alice的公钥后执行以下代码
    shared_key = private_key.exchange(ec.ECDH(), public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(shared_key)
    return derived_key


def aes_encrypt(key, data):
    cipher = AESGCM(key)
    ciphertext = cipher.encrypt(nonce, data, None)
    return ciphertext


def aes_decrypt(key, data):
    cipher = AESGCM(key)
    plaintext = cipher.decrypt(nonce, data, None)
    return plaintext


# #将公私钥对转换为字符串
# def key_to_string(private_key, public_key):
#     private_key_str = private_key.private_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PrivateFormat.PKCS8,
#         encryption_algorithm=serialization.NoEncryption()
#     )
#     public_key_str = public_key.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     )
#     return private_key_str, public_key_str


# #将字符串转换为公私钥对
# def string_to_key(private_key_str, public_key_str):
#     private_key = serialization.load_pem_private_key(
#         private_key_str,
#         password=None,
#         backend=default_backend()
#     )
#     public_key = serialization.load_pem_public_key(
#         public_key_str,
#         backend=default_backend()
#     )
#     return private_key, public_key


def key_to_string(private_key, public_key):
    """
    将ECC密钥对转化为字符串
    :param private_key: ECC私钥
    :param public_key: ECC公钥
    :return: 字符串形式的ECC密钥对
    """
    # 将私钥序列化为字符串
    private_key_str = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    # 将公钥序列化为字符串
    public_key_str = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    # 返回字符串形式的ECC密钥对
    return private_key_str, public_key_str


def string_to_key(private_key_str, public_key_str):
    """
    将字符串形式的ECC密钥对转化为ECC密钥对
    :param private_key_str: 字符串形式的ECC私钥
    :param public_key_str: 字符串形式的ECC公钥
    :return: ECC私钥和ECC公钥
    """
    # 将私钥字符串反序列化为私钥
    private_key = serialization.load_pem_private_key(
        data=private_key_str.encode(),
        password=None
    )

    # 将公钥字符串反序列化为公钥
    public_key = serialization.load_pem_public_key(
        data=public_key_str.encode()
    )

    # 返回ECC密钥对
    return private_key, public_key




if __name__ == '__main__':
    # 生成ECC密钥对
    private_key = ec.generate_private_key(ec.SECP384R1())
    public_key = private_key.public_key()

    # 将ECC密钥对转化为字符串
    private_key_str, public_key_str = key_to_string(private_key, public_key)

    # 将字符串形式的ECC密钥对转化为ECC密钥对
    #loaded_private_key, loaded_public_key = string_to_key(private_key_str, public_key_str)

    # 验证是否一致
    new_private_key, new_public_key = string_to_key(private_key_str, public_key_str)

    assert private_key.private_numbers().private_value == new_private_key.private_numbers().private_value
    assert public_key.public_numbers().x == new_public_key.public_numbers().x
    assert public_key.public_numbers().y == new_public_key.public_numbers().y
    # # 生成Alice的ECC密钥对
    # alice_private_key, alice_public_key = generate_ecc_key()
    # 生成Bob的ECC密钥对
    # bob_private_key, bob_public_key = generate_ecc_key()
    # # 假设Alice想要给Bob发送消息，Alice讲alice_public_key发送给Bob，首先需要生成共享密钥
    # derived_key = generate_shared_key(bob_private_key, alice_public_key)
    # print("共享密钥：", derived_key)
    # # 加密
    # data = bytes(input("Enter the message to encrypt: "), 'utf-8')
    # ciphertext = aes_encrypt(derived_key, data)
    # print("密文：", ciphertext)
    # # 解密
    # plaintext = aes_decrypt(derived_key, ciphertext)
    # print("明文：", str(plaintext, 'utf-8'))
    #print(generate_shared_key(bob_private_key, alice_public_key) == generate_shared_key(alice_private_key, bob_public_key))
    # alice_private_key_str, alice_public_key_str = key_to_string(alice_private_key, alice_public_key)
    # alice_private_key_fromstr, alice_public_key_fromstr = string_to_key(alice_private_key_str, alice_public_key_str)
    # print(alice_private_key == alice_private_key_fromstr)
    # print(key_to_string(bob_private_key, bob_public_key))

# # 使用派生的密钥创建AES-GCM加密器和解密器
# cipher = AESGCM(derived_key)
# decryptor = AESGCM(derived_key)
#
# # 使用加密器加密消息
# ciphertext = cipher.encrypt(nonce, plaintext, None)
#
# # 使用解密器解密消息
# plaintext = decryptor.decrypt(nonce, ciphertext, None)




