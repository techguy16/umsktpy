import argparse
from umsktjson import *

def process_options():
    parser = argparse.ArgumentParser(description="umskt ")
    parser.add_argument("-b", "--binkid", type=str, help="specify which BINK identifier to load (defaults to 2E)")
    parser.add_argument("-c", "--channelid", type=int, help="specify which Channel Identifier to use (defaults to 640)")
    parser.add_argument("-f", "--file", type=str, help="specify which keys file to load")

    args = parser.parse_args()
    return args

def main():
    args = process_options()
    
    if args.file is None:
            args.file = "keys.json"
            
    if args is not None:
        if args.channelid is None:
            args.channelid = 640
        
        print(generate_key(keysfile=args.file, bink=args.binkid, pid=args.channelid))
    if args is None:
        print(generate_key())

if __name__ == "__main__":
    main()

