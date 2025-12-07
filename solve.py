"""Recover RSA primes from two linear equations and decrypt the ciphertext.

The challenge output provides two linear combinations of the primes ``p`` and ``q``.
This script parses those coefficients, solves the 2x2 system with Cramer's rule to
get the primes, derives the private exponent, and prints the decrypted flag.
"""

import argparse
import re
from fractions import Fraction

def parse_values(path: str):
    with open(path) as f:
        data = f.read()
    numbers = re.findall(r"[0-9]+", data)
    keys = [
        "N",
        "e",
        "ct",
        "a",
        "b",
        "c",
        "d",
        "x",
        "y",
    ]
    if len(numbers) < len(keys):
        raise ValueError("Input file missing expected numeric values")
    return {name: int(value) for name, value in zip(keys, numbers)}

def recover_primes(values):
    a, b, c, d = values["a"], values["b"], values["c"], values["d"]
    x, y = values["x"], values["y"]
    det = a * d - b * c
    if det == 0:
        raise ValueError("Non-invertible coefficient matrix")
    p = Fraction(x * d - b * y, det)
    q = Fraction(a * y - x * c, det)
    if p.denominator != 1 or q.denominator != 1:
        raise ValueError("Recovered primes are not integral")
    return int(p), int(q)

def rsa_decrypt(values, p, q):
    e, ct, n = values["e"], values["ct"], values["N"]
    phi = (p - 1) * (q - 1)
    d_key = pow(e, -1, phi)
    m = pow(ct, d_key, n)
    return m.to_bytes((m.bit_length() + 7) // 8, "big")

def main():
    parser = argparse.ArgumentParser(description="Recover BabyRSA plaintext from the provided output file")
    parser.add_argument(
        "path",
        nargs="?",
        default="output.txt",
        help="Path to the challenge output (default: output.txt)",
    )
    args = parser.parse_args()

    values = parse_values(args.path)
    p, q = recover_primes(values)
    assert p * q == values["N"], "Recovered primes do not multiply to N"
    plaintext = rsa_decrypt(values, p, q)
    print(plaintext.decode())

if __name__ == "__main__":
    main()
