import argparse
from umskt import *
from umskt.mod7 import KeyGenerator
from umskt.mod7 import *

nothing = ""
def process_options():
    parser = argparse.ArgumentParser(description="usage: umsktpy ", usage=argparse.SUPPRESS)
    binkkeys = parser.add_argument_group('BINK keys')
    binkkeys.add_argument("-b","--binkid", metavar=nothing, type=str, help="Bink ID option")
    binkkeys.add_argument("-c","--channelid", metavar=nothing, type=int, help="Channel ID option")
    binkkeys.add_argument("-f","--file", metavar=nothing, type=str, help="File option")
    binkkeys.add_argument("-V","--verify", metavar=nothing, type=str, help="future use")
    binkkeys.add_argument("-i","--instid", metavar=nothing, type=str, help="future use")
    binkkeys.add_argument("-v","--verbose",action="store_true",help="enable verbose output")
    binkkeys.add_argument("-l","--list",action="store_true",help="show which products/binks can be loaded")
    mod7keys = parser.add_argument_group('mod7 keys')
    mod7keys.add_argument("-r", "--retail",action="store_true", help="win95 retail")
    mod7keys.add_argument("-o", "--oem",action="store_true",  help="win95 oem")
    mod7keys.add_argument("-e", "--retail11",action="store_true",  help="nt4")

    args = parser.parse_args()
    
    return args

def main():
    args = process_options()
    
    if args.list is None:
        args.list = False
        
    if args is not None and args.verify is None and args.list == False and args.retail is None and args.oem is None and args.retail11 is None:
        if args.channelid is None:
            args.channelid = 640
        if args.file is None:
            args.file = "keys.json"
        if args.binkid is None:
            args.binkid = "2E"
        if args.verbose is None:
            args.verbose = False
        
        key = generate_key(keysfile=args.file, bink=args.binkid, pid=args.channelid, verbose=args.verbose)
        if len(key) == 24:
            key = generate_key(keysfile=args.file, bink=args.binkid, pid=args.channelid)
        print(key)
        
    if args.verify is not None:
        if args.channelid is None:
            args.channelid = 640_696969
        if args.file is None:
            args.file = "keys.json"
        if args.binkid is None:
            args.binkid = "2E"
        print(validate_key(args.verify, args.channelid, args.binkid, args.file))
        
    if args is not None and args.list == True:
        listkeys()
    
    if args.retail:
        print(KeyGenerator.retailkey())
    if args.oem:
        print(KeyGenerator.oemkey())
    if args.retail11:
        print(elevendigitkey_a())
          
    if args is None:
        key = generate_key()
        if len(key) == 24:
            key = generate_key()
        print(key)

if __name__ == "__main__":
    main()

