import hashlib
import random
import secrets
import json

KCHARS = "BCDFGHJKMPQRTVWXY2346789"

def int_to_bytes(n, l=None):
    n = int(n)

    if not l:
        l = (n.bit_length() + 7) // 8

    return n.to_bytes(l, byteorder="little")

def encode_pkey(n):
    KCHARS = "BCDFGHJKMPQRTVWXY2346789"
    out = ""

    while n > 0:
        out = KCHARS[n % 24] + out
        n //= 24

    out = "-".join([out[i:i+5] for i in range(0, len(out), 5)])
    return out

def decode_pkey(k):
    k = k.replace("-", "")
    out = 0
    
    for c in k:
        out *= 24
        out += KCHARS.index(c)
    
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

def generate_key(keysfile="keys.json", bink="2E", pid=756, verbose=False):
    if verbose == True:
        print("Loading internal keys file")
        
    try:
        with open(keysfile) as json_file:
            binkdata = json.load(json_file)
            if verbose:
                print("Loaded internal keys file successfully")
    except FileNotFoundError:
        print("The specified file was not found.")
    except json.JSONDecodeError:
        print("There was an error decoding the JSON content.")
    except Exception as e:
        print("An unexpected error occurred:", e)
    
    bink_data = binkdata["BINK"][bink]
    if verbose:
        print("-----------------------------------------------------------")
        print("Loaded the following elliptic curve parameters: BINK[" + bink + "]")
        print("-----------------------------------------------------------")
        
    key_data = {
        "p": int(bink_data["p"]),
        "a": int(bink_data["a"]),
        "b": int(bink_data["b"]),
        "g": [
            int(bink_data["g"]["x"]),
            int(bink_data["g"]["y"])
        ],
        "pub": [
            int(bink_data["pub"]["x"]),
            int(bink_data["pub"]["y"])
        ],
        "n": int(bink_data["n"]),
        "priv": int(bink_data["priv"])
    }
    
    if verbose == True:
        print("P: ", bink_data["p"])
        print("a: ", bink_data["a"])
        print("b: ", bink_data["b"])
        print("Gx: ", bink_data["g"]["x"])
        print("Gy: ", bink_data["g"]["y"])
        print("Kx: ", bink_data["pub"]["x"])
        print("Ky: ", bink_data["pub"]["y"])
        print("n: ", bink_data["n"])
        print("k: ", bink_data["priv"])
        
    p = key_data["p"]
    a = key_data["a"]
    b = key_data["b"]
    B = key_data["g"]
    K = tuple(key_data["pub"])
    order = key_data["n"]
    private_key = -key_data["priv"] % order

    pid = int(str(pid) + "696969")
    if verbose:
        print("\n> Product ID: PPPPP-" + str(pid)[0:3] + "-" + str(pid)[3:] + "-23xxx\n")
    KCHARS = "BCDFGHJKMPQRTVWXY2346789"

    pid <<= 1

    while True:
        k = secrets.randbelow(p - 1) + 1
        r = scalar_mult(k, B, p, a)
        x, y = r

        md = hashlib.sha1(int_to_bytes(pid, 4) + int_to_bytes(x, 48) + int_to_bytes(y, 48)).digest()
        h = int.from_bytes(md[:4], byteorder="little") >> 4
        h &= 0xfffffff

        s = int(abs((private_key * h + k) % order))
        raw_pkey = s << 59 | h << 31 | pid

        if raw_pkey >> 96 < 0x40000:
            break
    
    if verbose:
        key = encode_pkey(raw_pkey) + "\n\nSuccess count:1/1"
    else:
        key = encode_pkey(raw_pkey)
    return key

def validate_key(pkey, pid, bink="2E", keysfile='keys.json'):
    with open(keysfile) as json_file:
        binkdata = json.load(json_file)
    
    bink_data = binkdata["BINK"][bink]
    
    B = tuple(bink_data["g"])
    K = tuple(bink_data["pub"])
    
    raw_pkey = decode_pkey(pkey)

    kpid = (raw_pkey & 0x7fffffff) >> 1
    verify = (kpid // 1000000) == ((pid >> 1) // 1000000)

    if verify:
        h = (raw_pkey >> 31) & 0xfffffff
        s = (raw_pkey >> 59) & 0x7ffffffffffffff

        r = h * K + s * B
        x, y = r.xy()

        md = hashlib.sha1(int_to_bytes(kpid << 1, 4) + int_to_bytes(x, 48) + int_to_bytes(y, 48)).digest()
        hp = int.from_bytes(md[:4], byteorder="little") >> 4
        hp &= 0xfffffff
        print(h, hp)

        if h == hp:
            print("Valid key")
        else:
            print("Invalid key")
            
def listkeys():
    with open("keys.json") as json_file:
        binkdata = json.load(json_file)
    
    bink_data = binkdata["Products"]

    # Sort the product keys alphabetically
    sorted_products = sorted(bink_data.keys())

    # List all items in the "Products" section alphabetically
    for product in sorted_products:
        details = bink_data[product]
        for key, value in details.items():
            if isinstance(value, list):
                formatted_value = ', '.join([f'"{item}"' for item in value])
                print(f"{product}: [{formatted_value}]")
            else:
                print(f"{product}: {value}")
            
    print("\n\n** Please note: any BINK ID other than 2E is considered experimental at this time **\n")
