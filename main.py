import argparse
from umsktjson import *

nothing = ""
def process_options():
    parser = argparse.ArgumentParser(description="usage: umskt ", usage=argparse.SUPPRESS)
    parser.add_argument("-b", "--binkid", metavar=nothing, type=str, help="Bink ID option")
    parser.add_argument("-c", "--channelid", metavar=nothing, type=int, help="Channel ID option")
    parser.add_argument("-f", "--file", metavar=nothing, type=str, help="File option")
    parser.add_argument("-V", "--verify", metavar=nothing, type=str, help="product key to validate signature")
    parser.add_argument("-v","--verbose",action="store_true",help="enable verbose output")
    parser.add_argument("-l","--list",action="store_true",help="show which products/binks can be loaded")

    args = parser.parse_args()
    return args

def main():
    args = process_options()
    
    if args.list is None:
        args.list = False
        
    if args is not None and args.verify is None and args.list == False:
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
            args.channelid = 640696969
        if args.file is None:
            args.file = "keys.json"
        if args.binkid is None:
            args.binkid = "2E"
        print(validate_key(args.verify, args.channelid, args.binkid, args.file))
        
    if args is not None and args.list == True:
        listkeys()
        
    if args is None:
        key = generate_key()
        if len(key) == 24:
            key = generate_key()
        print(key)

if __name__ == "__main__":
    main()

