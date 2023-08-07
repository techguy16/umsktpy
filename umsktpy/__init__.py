import hashlib
import random
import secrets

# JSON object for BINK data
key_data = {
    "p": 22604814143135632990679956684344311209819952803216271952472204855524756275151440456421260165232069708317717961315241,
    "a": 1,
    "b": 0,
    "g": [
        10910744922206512781156913169071750153028386884676208947062808346072531411270489432930252839559606812441712224597826,
        19170993669917204517491618000619818679152109690172641868349612889930480365274675096509477191800826190959228181870174
    ],
    "pub": [
        14399230353963643339712940015954061581064239835926823517419716769613937039346822269422480779920783799484349086780408,
        5484731395987446993229594927733430043632089703338918322171291299699820472711849119800714736923107362018017833200634
    ],
    "n": 61760995553426173,
    "priv": 37454031876727861
}

p = key_data["p"]
a = key_data["a"]
b = key_data["b"]
B = tuple(key_data["g"])
K = tuple(key_data["pub"])
order = key_data["n"]
private_key = -key_data["priv"] % order

# PID of product key
pid = 756_696969

# Key alphabet
KCHARS = "BCDFGHJKMPQRTVWXY2346789"

def int_to_bytes(n, l=None):
    n = int(n)

    if not l:
        l = (n.bit_length() + 7) // 8

    return n.to_bytes(l, byteorder="little")

def encode_pkey(n):
    out = ""

    while n > 0:
        out = KCHARS[n % 24] + out
        n //= 24

    out = "-".join([out[i:i+5] for i in range(0, len(out), 5)])
    return out

def inverse_mod(k, p):
    return pow(k, -1, p)

def add_points(P, Q, p, a):
    if P is None:
        return Q
    if Q is None:
        return P

    if P[0] == Q[0] and (P[1] + Q[1]) % p == 0:
        return None

    if P != Q:
        lam = ((Q[1] - P[1]) * inverse_mod(Q[0] - P[0], p)) % p
    else:
        lam = ((3 * P[0] * P[0] + a) * inverse_mod(2 * P[1], p)) % p

    x = (lam * lam - P[0] - Q[0]) % p
    y = (lam * (P[0] - x) - P[1]) % p
    return (x, y)

def scalar_mult(k, P, p, a):
    R = None
    for i in range(384):
        if k & (1 << i):
            R = add_points(R, P, p, a)
        P = add_points(P, P, p, a)
    return R

pid <<= 1

while True:
    k = secrets.randbelow(p - 1) + 1  # Generate a random k in the range [1, p-1]
    r = scalar_mult(k, B, p, a)
    x, y = r

    md = hashlib.sha1(int_to_bytes(pid, 4) + int_to_bytes(x, 48) + int_to_bytes(y, 48)).digest()
    h = int.from_bytes(md[:4], byteorder="little") >> 4
    h &= 0xfffffff

    s = int(abs((private_key * h + k) % order))
    raw_pkey = s << 59 | h << 31 | pid

    if raw_pkey >> 96 < 0x40000:
        break
        
print(encode_pkey(raw_pkey))

