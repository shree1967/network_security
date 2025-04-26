

import random
from math import gcd

# Miller-Rabin primality test
def is_prime(n, k=5):  # Number of tests
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):  # Perform k iterations of testing
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Generate large prime number
def generate_large_prime(bit_length):
    while True:
        num = random.getrandbits(bit_length)
        if num % 2 == 0:
            num += 1  # Ensure it's odd
        if is_prime(num):
            return num

# Extended Euclidean Algorithm for modular inverse
def mod_inverse(e, phi):
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x

    g, x, _ = egcd(e, phi)
    if g != 1:
        raise ValueError("No modular inverse exists")
    return x % phi

# Generate RSA key pair
def generate_keypair(bit_length):
    p = generate_large_prime(bit_length // 2)
    q = generate_large_prime(bit_length // 2)
    while q == p:  # Ensure p and q are distinct
        q = generate_large_prime(bit_length // 2)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Generate random e such that gcd(e, phi) = 1
    while True:
        e = random.randint(2, phi - 1)
        if gcd(e, phi) == 1:
            break

    d = mod_inverse(e, phi)

    return ((e, n), (d, n))

# Encrypt message
def encrypt(msg_plaintext, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in msg_plaintext]

# Decrypt message
def decrypt(msg_ciphertext, private_key):
    d, n = private_key
    return ''.join(chr(pow(char, d, n)) for char in msg_ciphertext)

# Driver program
if __name__ == "__main__":
    bit_length = int(input("Enter key bit-length (e.g., 1024): "))
    print("Generating RSA keys...")
    
    public, private = generate_keypair(bit_length)
    
    print("Public Key: ", public)
    print("Private Key: ", private)
    
    msg = input("Enter message to encrypt: ")
    encrypted_msg = encrypt(msg, public)
    
    print("\nEncrypted Message:")
    print(' '.join(map(str, encrypted_msg)))
    
    decrypted_msg = decrypt(encrypted_msg, private)
    
    print("\nDecrypted Message:")
    print(decrypted_msg)


