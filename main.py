#/usr/bin/python3

import argparse
from umsktjson import *

def process_options():
    nothing = ""
    parser = argparse.ArgumentParser(description="umskt ", usage=nothing)
    parser.add_argument("-b", "--binkid", metavar=nothing, type=str, help="specify which BINK identifier to load (defaults to 2E)")
    parser.add_argument("-c", "--channelid", metavar=nothing, type=int, help="specify which Channel Identifier to use (defaults to 640)")
    parser.add_argument("-f", "--file", metavar=nothing, type=str, help="specify which keys file to load")

    args = parser.parse_args()
    return args

def main():
    args = process_options()
    
    if args.file is None:
            args.file = "keys.json"
            
    if args.binkid is None:
    	args.binkid = "2E"
    
    if args is not None:
        if args.channelid is None:
            args.channelid = 640
        
        print(generate_key(keysfile=args.file, bink=args.binkid, pid=args.channelid))
    if args is None:
        print(generate_key())

if __name__ == "__main__":
    main()
