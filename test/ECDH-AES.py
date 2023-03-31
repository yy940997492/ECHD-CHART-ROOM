from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from os import urandom

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


if __name__ == '__main__':
    # 生成Alice的ECC密钥对
    alice_private_key, alice_public_key = generate_ecc_key()
    # 生成Bob的ECC密钥对
    bob_private_key, bob_public_key = generate_ecc_key()
    # 假设Alice想要给Bob发送消息，Alice讲alice_public_key发送给Bob，首先需要生成共享密钥
    derived_key = generate_shared_key(bob_private_key, alice_public_key)
    print("共享密钥：", derived_key)
    # 加密
    data = bytes(input("Enter the message to encrypt: "), 'utf-8')
    ciphertext = aes_encrypt(derived_key, data)
    print("密文：", ciphertext)
    # 解密
    plaintext = aes_decrypt(derived_key, ciphertext)
    print("明文：", str(plaintext, 'utf-8'))

# # 使用派生的密钥创建AES-GCM加密器和解密器
# cipher = AESGCM(derived_key)
# decryptor = AESGCM(derived_key)
#
# # 使用加密器加密消息
# ciphertext = cipher.encrypt(nonce, plaintext, None)
#
# # 使用解密器解密消息
# plaintext = decryptor.decrypt(nonce, ciphertext, None)




