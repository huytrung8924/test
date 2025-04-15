#! /usr/bin/env python3

import argparse
import sys
from sympy import factorint
from math import gcd

parser = argparse.ArgumentParser(description="RSA Common modulus attack")
required_named = parser.add_argument_group("required named arguments")
required_named.add_argument("-n", "--modulus", help="Common modulus", type=int, required=True)
required_named.add_argument("-e1", "--e1", help="First exponent", type=int, required=True)
required_named.add_argument("-e2", "--e2", help="Second exponent", type=int, required=True)
required_named.add_argument("-ct", "--ct", help="First ciphertext", type=int, required=True)
# required_named.add_argument("-d2", "--d2", help="D", type=int, required=True)
parser.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("-of", "--outputformat", type=str, choices=["decimal", "hex", "base64", "quoted", "ascii", "utf-8", "raw"], default="quoted")


def modinv(a, m):
    return pow(a, -1, m)
def check(m,e,n,c):
    c1=pow(m,e,n)
    return c1==c
def find_d2(e2,n):
    factors = factorint(n)  
    primes = list(factors.keys())
    if len(primes) == 2:
        phi_n = (primes[0] - 1) * (primes[1] - 1)
        d2 = pow(e2, -1, phi_n)  
        return d2
    else:
        raise ValueError("Cann't find D2")

def extended_gcd(a, b):#extended_Ecliud
        return gcd, x, y
def attack(c, e1, e2,d2, N):
    return m


def main():
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    quiet = args.quiet
    if quiet is None:
        quiet = False
    if not quiet:
        print("Starting the attack...")
    if gcd(args.ct, args.modulus) != 1:
        print("c and n must be coprime!", file=sys.stderr)
        sys.exit(1)

    message1 = attack(args.ct, args.e1, args.e2,find_d2(args.e2,args.modulus), args.modulus)
    message2 = check(message1,args.e1,args.modulus,args.ct)
    a1 = int.to_bytes(message1, (message1.bit_length() + 7) // 8, byteorder="big")

    if (message2):
        
        of = args.outputformat
        if of == "decimal" :
            b1 = a1
        elif of == "hex":
            import binascii

            b1 = binascii.hexlify(a1).decode("ascii")
        elif of == "base64":
            import base64

            b1 = base64.b64encode(a1).decode("ascii")
        elif of == "quoted":
            b1 = a1
        elif of == "ascii":
            b1 = a1.decode("ascii")
        elif of == "utf-8":
            b1 = a1.decode("utf-8")
        elif of == "raw":
            pass
        else:
            print("Unknown output format!", file=sys.stderr)
            sys.exit(1)
    else:
        if of == "raw":
            pass
        else:
            print("Plaintext message1: ", b1, file=sys.stderr)
            print("Decrypted messages must be the same!", file=sys.stderr)
            sys.exit(1)


    if not quiet:
        print("Attack complete.")
        print("Plaintext message:")

    if of == "raw":
        sys.stdout.buffer.write(a1)
    else:
        print(b1)


main()

