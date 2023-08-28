import argparse
import sys
from umskt import *
from umskt.mod7 import KeyGenerator
from umskt.mod7 import *

def process_options():
    parser = argparse.ArgumentParser(description="usage: umsktpy ", usage=argparse.SUPPRESS)
    binkkeys = parser.add_argument_group('BINK keys')
    binkkeys.add_argument("-b", "--binkid", metavar='', type=str, help="Bink ID option")
    binkkeys.add_argument("-c", "--channelid", metavar='', type=int, help="Channel ID option")
    binkkeys.add_argument("-f", "--file", metavar='', type=str, help="File option")
    binkkeys.add_argument("-V", "--verify", metavar='', type=str, help="future use")
    binkkeys.add_argument("-i", "--instid", metavar='', type=str, help="future use")
    binkkeys.add_argument("-v", "--verbose", action="store_true", help="enable verbose output")
    binkkeys.add_argument("-l", "--list", action="store_true", help="show which products/binks can be loaded")
    mod7keys = parser.add_argument_group('mod7 keys')
    mod7keys.add_argument("-r", "--retail", action="store_true", help="win95 retail")
    mod7keys.add_argument("-o", "--oem", action="store_true", help="win95 oem")
    mod7keys.add_argument("-e", "--retail11", action="store_true", help="nt4/office 97")
    mod7keys.add_argument("-m", "--mod7verify", metavar='', type=str, help="verification for mod7 keys")

    args = parser.parse_args()

    return args

def main():
    args = process_options()
    # print(args)

    if args.list == True:
        listkeys()
        sys.exit()
    if args.file is None:
        args.file = 'keys.json'
    if args.binkid is None:
        args.binkid = "2E"
    if args.channelid is None:
        args.channelid = 640
    if not args.verbose:
        args.verbose = False

    if args.retail:
        print(KeyGenerator.retailkey())
    if args.oem:
        print(KeyGenerator.oemkey())
    if args.retail11:
        print(elevendigitkey_a())
    if args.mod7verify:
        verify_mod7(args.mod7verify)

    if args.binkid or args.channelid or args.file or args.verbose and args.retail == False and args.oem == False and args.retail11 == False and args.mod7verify == False and args.list == False:
        if args.verbose:
            key = generate_key(keysfile=args.file, bink=args.binkid, pid=args.channelid, verbose=True)
        else:
            key = generate_key(keysfile=args.file, bink=args.binkid, pid=args.channelid)
        print(key)

    if args.verify:
        print(validate_key(args.verify))

    if not any(vars(args).values()) and not args.list:
        key = generate_key()
        if len(key) == 24:
            key = generate_key()
        print(key)

if __name__ == "__main__":
    main()