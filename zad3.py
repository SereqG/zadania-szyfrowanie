import string

def vigenere_encrypt(text, key):
    alphabet = string.ascii_uppercase
    text = text.replace(" ", "").upper()
    key = key.upper()

    encrypted = []
    key_index = 0

    for ch in text:
        if ch in alphabet:
            shift = alphabet.index(key[key_index % len(key)])
            new_char = alphabet[(alphabet.index(ch) + shift) % 26]
            encrypted.append(new_char)
            key_index += 1

    return "".join(encrypted)


def vigenere_decrypt(cipher, key):
    alphabet = string.ascii_uppercase
    cipher = cipher.upper()
    key = key.upper()

    decrypted = []
    key_index = 0

    for ch in cipher:
        if ch in alphabet:
            shift = alphabet.index(key[key_index % len(key)])
            new_char = alphabet[(alphabet.index(ch) - shift) % 26]
            decrypted.append(new_char)
            key_index += 1

    return "".join(decrypted)


def key_cycle_length(message_length, key_length):
    from math import gcd
    return key_length * message_length // gcd(message_length, key_length)

if __name__ == "__main__":

    text = "INFORMATYKA"
    key1 = "KOD"
    key2 = "PROGRAMOWANIE"

    print("===== Szyfr Vigenère'a — pełne rozwiązanie =====\n")

    cipher1 = vigenere_encrypt(text, key1)
    decipher1 = vigenere_decrypt(cipher1, key1)

    print("Tekst:", text)
    print("Klucz:", key1)
    print("Szyfrogram:", cipher1)
    print("Odszyfrowane:", decipher1)

    cipher2 = vigenere_encrypt(text, key2)
    decipher2 = vigenere_decrypt(cipher2, key2)

    print("\nTekst:", text)
    print("Klucz:", key2)
    print("Szyfrogram:", cipher2)
    print("Odszyfrowane:", decipher2)

    print("\n===== Porównanie szyfrogramów =====")
    print("Szyfrogram dla klucza KOD:", cipher1)
    print("Szyfrogram dla klucza PROGRAMOWANIE:", cipher2)

    print("\n===== Długość cyklu powtarzania klucza =====")
    for length in [10, 20, 30]:
        cycle = key_cycle_length(length, len(key1))
        print(f"Długość tekstu: {length:2d} | Klucz: {key1} (len={len(key1)}) → cykl: {cycle}")
