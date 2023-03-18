from Crypto.Cipher import AES


# AES Encryption
def aes_encrypt(key, data):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce, ciphertext, tag


# AES Decryption
def aes_decrypt(key, nonce, ciphertext, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        # print("The message is authentic:", plaintext)
        return plaintext
    except ValueError:
        print("Key incorrect or message corrupted")


# Main
if __name__ == '__main__':
    data = bytes(input("Enter the message to encrypt: "), 'utf-8')
    key = bytes(input("Enter the key: "), 'utf-8')
    nonce, ciphertext, tag = aes_encrypt(key, data)
    print("密文：", ciphertext)
    plaintext = aes_decrypt(key, nonce, ciphertext, tag)
    print(str(plaintext, 'utf-8'))
