from utils.texts import wikipedia_text, text_10, text_100, text_1000, text_100000

def caesar_cipher(text, shift):
    result = ""

    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char

    return result

def caesar_cipher_polish(text, shift):
    result = ""
    
    polish_alphabet_upper = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ"
    polish_alphabet_lower = "aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż"
    
    for char in text:
        if char in polish_alphabet_upper:
            old_index = polish_alphabet_upper.index(char)
            new_index = (old_index + shift) % len(polish_alphabet_upper)
            result += polish_alphabet_upper[new_index]
        elif char in polish_alphabet_lower:
            old_index = polish_alphabet_lower.index(char)
            new_index = (old_index + shift) % len(polish_alphabet_lower)
            result += polish_alphabet_lower[new_index]
        else:
            result += char
    
    return result

def brute_force_polish(encrypted_text):
    print("=== ATAK BRUTE-FORCE - ULEPSZONY SZYFR POLSKI ===")
    print(f"Zaszyfrowany tekst: {encrypted_text}")
    print("=" * 55)

    polish_althabet_length = 32
    
    for shift in range(1, polish_althabet_length + 1):
        decrypted = caesar_cipher_polish(encrypted_text, -shift)
        
        if "język" in decrypted.lower() or "polski" in decrypted.lower() or "świetny" in decrypted.lower():
            print(f"Przesunięcie {shift:2d}: {decrypted} ← *** POPRAWNY WYNIK! ***")
        else:
            print(f"Przesunięcie {shift:2d}: {decrypted}")
    
    print("=" * 55)
    return None

def brute_force_caesar(encrypted_text):
    print(f"Zaszyfrowany tekst: {encrypted_text}")
    
    for shift in range(1, 26):
        decrypted = caesar_cipher(encrypted_text, -shift)
        
        if "INFORMATYKA" in decrypted or "JEST" in decrypted or "SUPER" in decrypted:
            print(f"Przesunięcie {shift:2d}: {decrypted} ← *** POPRAWNY WYNIK! ***")
        else:
            print(f"Przesunięcie {shift:2d}: {decrypted}")
    
    print("=" * 50)
    return None

def decrypt_caesar_with_shift(encrypted_text, shift):
    return caesar_cipher(encrypted_text, -shift)

original_text = 'INFORMATYKA JEST SUPER'
encrypted = caesar_cipher(original_text, 3)

print(f"=== SZYFR CEZARA (bez polskich znaków) ===")
print(f"Oryginalny tekst: {original_text}")
print(f"Zaszyfrowany tekst: {encrypted}")
print(f"Odszyfrowany (przesunięcie 3): {decrypt_caesar_with_shift(encrypted, 3)}")
print("=== ATAK BRUTE-FORCE NA SZYFR CEZARA ===")
print("=" * 50)
brute_force_caesar(encrypted)

polish_encrypted = caesar_cipher_polish(original_text, 7)

print(f"=== SZYFR CEZARA (z polskimi znakami) ===")
print(f"Oryginalny tekst: {original_text}")
print(f"Zaszyfrowany tekst: {polish_encrypted}")
print(f"Odszyfrowany: {caesar_cipher_polish(polish_encrypted, -7)}")

print(f"=== SZYFR CEZARA (z polskimi znakami) - TEST Z WIKIPEDII ===")
wikipedia_encrypted = caesar_cipher_polish(wikipedia_text, 5)
print(f"Zaszyfrowany tekst z Wikipedii: {wikipedia_encrypted[:60]}...") 

# ========================================
# TESTY WYDAJNOŚCI BRUTE-FORCE
# ========================================

import time
import random

def measure_brute_force_time(text, shift_used=None):
    """Mierzy czas wykonania ataku brute-force na tekście"""
    if shift_used is None:
        shift_used = random.randint(1, 25)
    
    print(f"\n=== ATAK BRUTE-FORCE - DŁUGOŚĆ TEKSTU: {len(text)} znaków ===")
    print(f"Fragment tekstu: {text[:50]}{'...' if len(text) > 50 else ''}")
    print(f"Użyte przesunięcie: {shift_used}")
    
    encrypted = caesar_cipher(text.upper(), shift_used)
    print(f"Fragment zaszyfrowanego: {encrypted[:50]}{'...' if len(encrypted) > 50 else ''}")
    
    start_time = time.time()
    found_solution = False
    attempts = 0
    
    for shift in range(1, 26):
        attempts += 1
        decrypted = caesar_cipher(encrypted, -shift)
        
        if any(word in decrypted.upper() for word in ['ALGORYTMY', 'KRYPTOGRA', 'TEKST', 'PRZYKLADOWY', 'TO', 'JEST']):
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"✓ ZNALEZIONO! Przesunięcie: {shift}, Prób: {attempts}, Czas: {elapsed_time:.6f}s")
            print(f"  Fragment odszyfr.: {decrypted[:80]}{'...' if len(decrypted) > 80 else ''}")
            found_solution = True
            break
    
    if not found_solution:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"✗ Nie znaleziono, Prób: {attempts}, Czas: {elapsed_time:.6f}s")
    
    print("=" * 60)

print("\n" + "TESTY WYDAJNOŚCI ATAKU BRUTE-FORCE (LOSOWE PRZESUNIĘCIA)")
print("=" * 60)

random.seed(42)
measure_brute_force_time(text_10)
measure_brute_force_time(text_100)  
measure_brute_force_time(text_1000)
measure_brute_force_time(text_100000)