from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import binascii
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def key_to_string(private_key, public_key):
    private_key_str = binascii.hexlify(private_key.private_bytes(encoding=serialization.Encoding.DER, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())).decode()
    public_key_str = binascii.hexlify(public_key.public_bytes(encoding=serialization.Encoding.DER, format=serialization.PublicFormat.SubjectPublicKeyInfo)).decode()
    return private_key_str, public_key_str


def string_to_key(private_key_str, public_key_str):
    private_key_bytes = binascii.unhexlify(private_key_str.encode())
    public_key_bytes = binascii.unhexlify(public_key_str.encode())
    private_key = serialization.load_der_private_key(private_key_bytes, password=None)
    public_key = serialization.load_der_public_key(public_key_bytes)
    return private_key, public_key



# def key_to_string(private_key, public_key):
#     """
#     将ECC密钥对转化为字符串
#     :param private_key: ECC私钥
#     :param public_key: ECC公钥
#     :return: 字符串形式的ECC密钥对
#     """
#     # 将私钥序列化为字符串
#     private_key_str = private_key.private_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PrivateFormat.PKCS8,
#         encryption_algorithm=serialization.NoEncryption()
#     ).decode()
#
#     # 将公钥序列化为字符串
#     public_key_str = public_key.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     ).decode()
#
#     # 返回字符串形式的ECC密钥对
#     return private_key_str, public_key_str
#
#
# def string_to_key(private_key_str, public_key_str):
#     """
#     将字符串形式的ECC密钥对转化为ECC密钥对
#     :param private_key_str: 字符串形式的ECC私钥
#     :param public_key_str: 字符串形式的ECC公钥
#     :return: ECC私钥和ECC公钥
#     """
#     # 将私钥字符串反序列化为私钥
#     private_key = serialization.load_pem_private_key(
#         data=private_key_str.encode(),
#         password=None
#     )
#
#     # 将公钥字符串反序列化为公钥
#     public_key = serialization.load_pem_public_key(
#         data=public_key_str.encode()
#     )
#
#     # 返回ECC密钥对
#     return private_key, public_key


# 生成ECC密钥对
# private_key = ec.generate_private_key(ec.SECP384R1())
# public_key = private_key.public_key()
#
# # 将ECC密钥对转化为字符串
# private_key_str, public_key_str = key_to_string(private_key, public_key)
#
# # 将字符串形式的ECC密钥对转化为ECC密钥对
# loaded_private_key, loaded_public_key = string_to_key(private_key_str, public_key_str)

# 验证是否一致
# assert private_key == loaded_private_key
# assert public_key == loaded_public_key

# 生成ECC密钥对
# private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
# public_key = private_key.public_key()
#
# # 将ECC密钥对转换为字符串
# private_key_str, public_key_str = key_to_string(private_key, public_key)
#
# # 将字符串转换回ECC密钥对
# new_private_key, new_public_key = string_to_key(private_key_str, public_key_str)
#
# # 验证结果是否正确
# # assert private_key.private_numbers().private_value == new_private_key.private_numbers().private_value
# # assert public_key.public_numbers().x == new_public_key.public_numbers().x
# # assert public_key.public_numbers().y == new_public_key.public_numbers().y
# print('ok')
# 生成ECC密钥对
# 生成ECC密钥对
private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
public_key = private_key.public_key()

# 将ECC密钥对转换为字符串
private_key_str, public_key_str = key_to_string(private_key, public_key)

# 将字符串转换回ECC密钥对
new_private_key, new_public_key = string_to_key(private_key_str, public_key_str)

assert private_key.private_numbers().private_value == new_private_key.private_numbers().private_value
assert public_key.public_numbers().x == new_public_key.public_numbers().x
assert public_key.public_numbers().y == new_public_key.public_numbers().y
