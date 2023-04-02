import json

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from os import urandom
import pickle
import os
from cryptography.hazmat.primitives import serialization
import binascii
nonce = urandom(12)


def generate_ecc_key():
    private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
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


# 将密文转化为字符串
def ciphertext_to_string(ciphertext):
    ciphertext_str = binascii.b2a_hex(ciphertext).decode()
    return ciphertext_str


# 将字符串转化为密文
def string_to_ciphertext(ciphertext_str):
    ciphertext = binascii.a2b_hex(ciphertext_str.encode())
    return ciphertext


if __name__ == '__main__':
    # 生成ECC密钥对
    alice_private_key, alice_public_key = generate_ecc_key()
    # bob_private_key, bob_public_key = generate_ecc_key()

    # 将ECC密钥对转换为字符串
    alice_private_key_str, alice_public_key_str = key_to_string(alice_private_key, alice_public_key)
    # bob_private_key_str, bob_public_key_str = key_to_string(bob_private_key, bob_public_key)
    print("alice's private:\n"+alice_private_key_str)
    print("alice's public:\n"+alice_public_key_str)
    # print("bob's private:\n"+bob_private_key_str)
    # print("bob's public:\n"+bob_public_key_str)

#     alice_private_key_str = '''-----BEGIN PRIVATE KEY-----
# MIG2AgEAMBAGByqGSM49AgEGBSuBBAAiBIGeMIGbAgEBBDBi0E0H6Huq0xUdx/9o
# HScYNhJ6VPyWIALpS0vIKVACd3o1MlohG4pKvVG3SrxqbFWhZANiAATqjCXdOORY
# /hnoZDskNcD5DU0LfsakXEmNJI4n1AWpaxDwVkNxaRu9luyRED4W901f7oGhE3gC
# pFMlFT3YzUS6+CTzLNje9RS0oYziSHlq1Tuh1I2bmSLM8TGaxzaxClU=
# -----END PRIVATE KEY-----'''
#     alice_public_key_str = '''-----BEGIN PUBLIC KEY-----
# MHYwEAYHKoZIzj0CAQYFK4EEACIDYgAE6owl3TjkWP4Z6GQ7JDXA+Q1NC37GpFxJ
# jSSOJ9QFqWsQ8FZDcWkbvZbskRA+FvdNX+6BoRN4AqRTJRU92M1Euvgk8yzY3vUU
# tKGM4kh5atU7odSNm5kizPExmsc2sQpV
# -----END PUBLIC KEY-----'''
#     bob_private_key_str = '''-----BEGIN PRIVATE KEY-----
# MIG2AgEAMBAGByqGSM49AgEGBSuBBAAiBIGeMIGbAgEBBDBYjZcCGdprT/fJmjUQ
# Z8dAUgKM5BAi/cotNU+fiZiRR2AZnBmaXRAb8umn0Ab6BP6hZANiAATTD5lhj86z
# V89XRNN9wmTEU8DnZR1vSXTmm7RU6ols/k7vSDItU2NNW5Hzgb/vpFblfSYGPptL
# F24THK68XQZuNAGMHJOUiSEbqTtijz5GtauXqDidNeRZOkcWfCXxixQ=
# -----END PRIVATE KEY-----'''
#     bob_public_key_str = '''-----BEGIN PUBLIC KEY-----
# MHYwEAYHKoZIzj0CAQYFK4EEACIDYgAE0w+ZYY/Os1fPV0TTfcJkxFPA52Udb0l0
# 5pu0VOqJbP5O70gyLVNjTVuR84G/76RW5X0mBj6bSxduExyuvF0GbjQBjByTlIkh
# G6k7Yo8+RrWrl6g4nTXkWTpHFnwl8YsU
# -----END PUBLIC KEY-----'''
#
#     # 将字符串形式的ECC密钥对转换为ECC密钥对
#     from_private_key, from_public_key = string_to_key(alice_private_key_str, alice_public_key_str)
#     # 获取BobBob的公钥
#     to_private_key, to_public_key = string_to_key(bob_private_key_str, bob_public_key_str)
#
#     # assert alice_private_key.private_numbers().private_value == new_alice_private_key.private_numbers().private_value
#     # assert alice_public_key.public_numbers().x == new_alice_public_key.public_numbers().x
#     # assert alice_public_key.public_numbers().y == new_alice_public_key.public_numbers().y
#
#     # 生成共享密钥
#     shared_key = generate_shared_key(from_private_key, to_public_key)
#     #new_shared_key = generate_shared_key(new_bob_private_key, new_alice_public_key)
#     # 加密消息
#     msg = 'Hello World!'
#     ciphertext = aes_encrypt(shared_key, msg.encode('utf-8'))
#     ciphertext_str = ciphertext_to_string(ciphertext)
#     # print(ciphertext_str)
#     msg = ciphertext_str
#     send_data = {
#         'msgText': msg,
#     }
#     socket_msg = json.dumps(send_data).encode()
#     back_msg = socket_msg.decode()
#     new_msg = json.loads(back_msg)
#
#     # 得到加密的字符串
#     new_ciphertext_str = new_msg['msgText']
#     # 将字符串转化为密文
#     new_ciphertext = string_to_ciphertext(new_ciphertext_str)
#     # 解密
#     plaintext = aes_decrypt(shared_key, new_ciphertext)
#     #new_plaintext = aes_decrypt(new_shared_key, ciphertext)
#
#     print(plaintext.decode('utf-8'))
#     print(nonce, '\n', type(nonce))