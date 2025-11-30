import string

def create_polibius_table(merge_ij=True):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" if merge_ij else string.ascii_uppercase.replace("Q", "")
    table = {}
    reverse = {}
    index = 0

    for row in range(1, 6):
        for col in range(1, 6):
            letter = alphabet[index]
            table[letter] = f"{row}{col}"
            reverse[f"{row}{col}"] = letter
            index += 1

    return table, reverse


def polibius_encrypt(text, table):
    text = text.upper().replace("J", "I")
    result = []
    for ch in text:
        if ch in table:
            result.append(table[ch])
    return " ".join(result)


def polibius_decrypt(cipher, reverse_table):
    parts = cipher.split()
    result = []
    for p in parts:
        if p in reverse_table:
            result.append(reverse_table[p])
    return "".join(result)


def create_keyword_table(keyword):
    keyword = keyword.upper().replace("J", "I")
    keyword = "".join(dict.fromkeys(keyword))

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    rest = "".join(c for c in alphabet if c not in keyword)

    full = keyword + rest

    table = {}
    reverse = {}
    index = 0

    for row in range(1, 6):
        for col in range(1, 6):
            letter = full[index]
            table[letter] = f"{row}{col}"
            reverse[f"{row}{col}"] = letter
            index += 1

    return table, reverse


if __name__ == "__main__":

    print("=== Klasyczna tablica Polibiusza ===")
    table, reverse_table = create_polibius_table()

    text = "POLITECHNIKA"
    encrypted = polibius_encrypt(text, table)
    decrypted = polibius_decrypt(encrypted, reverse_table)

    print("Tekst:", text)
    print("Szyfrogram:", encrypted)
    print("Odszyfrowane:", decrypted)

    print("\n=== Tablica ze słowem kluczowym POLI ===")
    key_table, key_reverse = create_keyword_table("POLI")

    encrypted_key = polibius_encrypt(text, key_table)
    decrypted_key = polibius_decrypt(encrypted_key, key_reverse)

    print("Tekst:", text)
    print("Szyfrogram (słowo kluczowe):", encrypted_key)
    print("Odszyfrowane:", decrypted_key)

    print("\n=== Porównanie ===")
    print("Klasyczna:", encrypted)
    print("Słowo POLI:", encrypted_key)
