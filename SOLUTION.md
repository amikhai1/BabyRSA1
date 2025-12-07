# BabyRSA Solver Explanation

This solver unpacks the "BabyRSA" challenge values, reconstructs the RSA primes from
linear equations, and decrypts the ciphertext. The key steps are:

1. **Parse challenge output**: Extract the numeric values (\(N, e, ct, a, b, c, d, x, y\))
   from `output.txt` using a simple regex. Order matters because the solver maps the
   first nine numbers to these names.
2. **Recover \(p\) and \(q\)**: The challenge provides two linear combinations of the
   unknown primes:
   \[
   \begin{cases}
   a p + b q = x \\
   c p + d q = y
   \end{cases}
   \]
   Solve this 2×2 system with Cramer's rule. The determinant \(ad - bc\) must be
   non-zero; otherwise the system has no unique solution. The code uses
   `fractions.Fraction` to ensure the result is integral—if either prime comes out with
   a non-unit denominator the solver aborts.
3. **Verify the modulus**: Confirm the recovered primes satisfy \(p \times q = N\) to
   catch any bad parsing or arithmetic issues.
4. **Derive the private key**: Compute \(\phi = (p-1)(q-1)\) and invert the public
   exponent via `pow(e, -1, phi)` to obtain the private exponent \(d\).
5. **Decrypt the ciphertext**: Use modular exponentiation to recover the plaintext and
   print it as bytes.

Running `python solve.py` reads `output.txt`, performs these steps, and prints the flag
`DawgCTF{wh0_s41d_m4th_15_us3l3ss?}`.
