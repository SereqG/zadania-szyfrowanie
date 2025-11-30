def xor_cipher(text, key):
    encrypted = []
    key_len = len(key)

    for i, char in enumerate(text):
        encrypted_char = ord(char) ^ ord(key[i % key_len])
        encrypted.append(encrypted_char)

    return encrypted


def xor_decipher(encoded, key):
    decrypted = []
    key_len = len(key)

    for i, val in enumerate(encoded):
        decrypted_char = chr(val ^ ord(key[i % key_len]))
        decrypted.append(decrypted_char)

    return "".join(decrypted)


text = "INFORMATYKA"
key = "KEY"

encrypted = xor_cipher(text, key)
print("Zaszyfrowane wartości:", encrypted)

decrypted = xor_decipher(encrypted, key)
print("Odszyfrowany tekst:", decrypted)
