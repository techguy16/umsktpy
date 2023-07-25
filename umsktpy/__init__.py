import os
import platform
from subprocess import PIPE, run
import re

def convertTuple(tup):
    str = ''.join(tup)
    return str

def find_umskt_executable():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os_name = platform.system()

    if os_name == "Windows":
        umskt_name = "umsktw.exe"
    elif os_name == "Darwin":  # Mac
        umskt_name = "umsktm"
    elif os_name == "Linux":
        umskt_name = "umsktl"
    elif os_name == "FreeBSD":
        umskt_name = "umsktf"
    else:
        raise OSError("Unsupported operating system. The 'umskt' executable is not available for this platform.")

    umskt_path = os.path.join(current_dir, umskt_name)

    if not os.path.exists(umskt_path):
        raise FileNotFoundError(f"The '{umskt_name}' executable was not found in the library directory for your operating system.")

    return umskt_path

def umskt(bink):
    umskt_path = find_umskt_executable()

    command = [umskt_path, "-b", bink]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    work = str(result.returncode), result.stdout, result.stderr

    r = convertTuple(work)
    r = r[1:31]
    r = r.rstrip()
    return r

def listbink():
    umskt_path = find_umskt_executable()

    command = [umskt_path, "-l"]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    work = str(result.returncode), result.stdout, result.stderr

    r = convertTuple(work)
    r = r.replace("** Please note: any BINK ID other than 2E is considered experimental at this time **", "")
    r = r[1:]
    r = re.sub(r'\n\s*\n','\n',r,re.MULTILINE)
    return r
    
def validate(key):
    umskt_path = find_umskt_executable()

    command = [umskt_path, "-V", key]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    work = str(result.returncode), result.stdout, result.stderr

    r = convertTuple(work)
    if 'Key validated successfully!' in r:
        r = True
    else:
        r = False
    
    return r
    
def installationid(id):
    umskt_path = find_umskt_executable()

    command = [umskt_path, "-i", id]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    work = str(result.returncode), result.stdout, result.stderr

    r = convertTuple(work)
    if 'ERROR: Installation ID checksum failed. Please check that it is typed correctly.' in r:
        r = 'Invalid Installation ID.'
    else:
        r = r[1:49]
    
    return r

