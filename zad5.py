import hashlib
import struct
import base64
import random
from typing import List


def _sha256_int(data: bytes) -> int:
    return int.from_bytes(hashlib.sha256(data).digest(), 'big')


def generate_sbox(key: str) -> List[int]:
    seed = _sha256_int(key.encode('utf-8') + b'sbox')
    rng = random.Random(seed)
    sbox = list(range(256))
    rng.shuffle(sbox)
    return sbox


def invert_sbox(sbox: List[int]) -> List[int]:
    inv = [0] * 256
    for i, v in enumerate(sbox):
        inv[v] = i
    return inv


def generate_keystream(key: str, length: int) -> bytes:
    out = bytearray()
    counter = 0
    key_bytes = key.encode('utf-8')
    while len(out) < length:
        h = hashlib.sha256(key_bytes + counter.to_bytes(4, 'big')).digest()
        out.extend(h)
        counter += 1
    return bytes(out[:length])


def block_permutation(key: str, block_size: int) -> List[int]:
    seed = _sha256_int(key.encode('utf-8') + b'perm' + block_size.to_bytes(2,'big'))
    rng = random.Random(seed)
    perm = list(range(block_size))
    rng.shuffle(perm)
    return perm


def apply_permutation_block(block: bytes, perm: List[int]) -> bytes:
    bs = bytearray(len(block))
    for i, src_idx in enumerate(perm):
        if src_idx < len(block):
            bs[i] = block[src_idx]
        else:
            bs[i] = 0
    return bytes(bs)


def invert_permutation(perm: List[int]) -> List[int]:
    inv = [0] * len(perm)
    for i, p in enumerate(perm):
        inv[p] = i
    return inv


def _block_size_from_key(key: str) -> int:
    L = len(key)
    return max(2, (L % 16) + 2)


def encrypt(plaintext: str, key: str) -> str:
    data = plaintext.encode('utf-8')
    orig_len = len(data)
    sbox = generate_sbox(key)
    sub = bytes([sbox[b] for b in data])
    ks = generate_keystream(key, orig_len)
    xored = bytes([b ^ ks[i] for i, b in enumerate(sub)])
    block_size = _block_size_from_key(key)
    perm = block_permutation(key, block_size)
    padding = (block_size - (len(xored) % block_size)) % block_size
    padded = xored + bytes(padding)
    out_blocks = []
    for i in range(0, len(padded), block_size):
        block = padded[i:i+block_size]
        out_blocks.append(apply_permutation_block(block, perm))
    body = b''.join(out_blocks)
    header = struct.pack('>Q', orig_len)
    cipher = header + body
    return base64.b64encode(cipher).decode('ascii')


def decrypt(cipher_b64: str, key: str) -> str:
    cipher = base64.b64decode(cipher_b64)
    if len(cipher) < 8:
        raise ValueError('Ciphertext too short')
    orig_len = struct.unpack('>Q', cipher[:8])[0]
    body = cipher[8:]
    block_size = _block_size_from_key(key)
    if len(body) % block_size != 0:
        pass
    perm = block_permutation(key, block_size)
    inv = invert_permutation(perm)
    blocks = []
    for i in range(0, len(body), block_size):
        block = body[i:i+block_size]
        bs = bytearray(len(block))
        for k in range(len(block)):
            bs[k] = block[inv[k]]
        blocks.append(bytes(bs))
    combined = b''.join(blocks)
    combined = combined[:orig_len]
    ks = generate_keystream(key, orig_len)
    xored = bytes([b ^ ks[i] for i, b in enumerate(combined)])
    inv_s = invert_sbox(generate_sbox(key))
    plain_bytes = bytes([inv_s[b] for b in xored])
    return plain_bytes.decode('utf-8', errors='replace')



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Hybrid cipher CLI for encrypt/decrypt using app5 library')
    mode = parser.add_mutually_exclusive_group(required=False)
    mode.add_argument('-e', '--encrypt', action='store_true', help='Encrypt input text/file (default)')
    mode.add_argument('-d', '--decrypt', action='store_true', help='Decrypt base64 input text/file')
    inp = parser.add_mutually_exclusive_group(required=False)
    inp.add_argument('-t', '--text', type=str, help='Input text to process')
    inp.add_argument('-i', '--infile', type=str, help='Path to input file (text, UTF-8)')
    parser.add_argument('-o', '--outfile', type=str, help='Write result to this file (otherwise printed)')
    parser.add_argument('-k', '--key', type=str, default='secret', help='Key string (default: secret)')
    args = parser.parse_args()

    if not args.text and not args.infile:
        parser.print_help()
        exit(1)

    is_encrypt = args.encrypt or not args.decrypt

    if args.infile:
        with open(args.infile, 'rb') as f:
            data = f.read()
        text = data.decode('utf-8')
    else:
        text = args.text or ''

    if is_encrypt:
        out = encrypt(text, args.key)
    else:
        out = decrypt(text, args.key)

    if args.outfile:
        mode_write = 'wb' if isinstance(out, (bytes, bytearray)) else 'w'
        with open(args.outfile, mode_write) as f:
            if isinstance(out, (bytes, bytearray)):
                f.write(out)
            else:
                f.write(out)
    else:
        if isinstance(out, (bytes, bytearray)):
            print(out.decode('utf-8'))
        else:
            print(out)