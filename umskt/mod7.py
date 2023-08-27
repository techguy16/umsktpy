import random
from abc import ABC


class KeyGenerator(ABC):
    @staticmethod
    def num_digits(num):
        ct = 0
        while num > 0:
            ct += 1
            num //= 10
        return ct

    @staticmethod
    def sum_of_digits(num):
        sm = 0
        while num > 0:
            rem = num % 10
            sm += rem
            num //= 10
        return sm

    # CD Key generator
    # Format: XXX-XXXXXXX
    # Rules:
    # Last seven digits must add to be divisible by 7
    # First 3 digits cannot be 333, 444,..., 999
    # Last digit of last seven digits cannot be 0, 8 or 9
    @staticmethod
    def retailkey():
        x1 = random.randint(0, 1000)
        while x1 % 111 == 0:
            x1 = random.randint(0, 1000)
        x1str = ""
        if x1 > 100:
            x1str = str(x1)
        if 10 < x1 < 100:
            x1str = "0" + str(x1)
        if x1 < 10:
            x1str = "00" + str(x1)
        x2 = 1
        while KeyGenerator.sum_of_digits(x2) % 7 != 0:
            x2 = random.randint(0, 10000000)
            while x2 % 10 == 0 or x2 % 10 == 8 or x2 % 10 == 9:
                x2 = random.randint(0, 10000000)
        length = KeyGenerator.num_digits(x2)
        x2str = ""
        for i in range(0, 7 - length):
            x2str += "0"
        x2str += str(x2)
        return x1str + "-" + x2str

    # Format: ABCYY-OEM-0XXXXXX-XXXXX
    # ABC is the day of the year. It can be any value from 001 to 366
    # YY is the last two digits of the year. It can be anything from 95 to 03
    # 0XXXXXX is a random number that has a sum that is divisible by 7 and does not end with 0, 8 or 3.
    # XXXXX is a random 5-digit number
    @staticmethod
    def oemkey():
        doy = random.randint(1, 367)
        length = KeyGenerator.num_digits(doy)
        doystring = ""
        for i in range(0, 3 - length):
            doystring += "0"
        doystring += str(doy)
        ystring = random.choice(["95", "96", "97", "98", "99", "00", "01", "02", "03"])
        x2 = 1
        x2str = "0"
        while KeyGenerator.sum_of_digits(x2) % 7 != 0:
            x2 = random.randint(0, 1000000)
            while x2 % 10 == 0 or x2 % 10 == 8 or x2 % 10 == 9:
                x2 = random.randint(0, 1000000)
        length = KeyGenerator.num_digits(x2)
        for i in range(0, 6 - length):
            x2str += "0"
        x2str += str(x2)
        x3 = random.randint(0, 100000)
        x3str = ""
        for i in range(0, 5 - length):
            x3str += "0"
        x3str += str(x3)
        return doystring + ystring + "-OEM-" + x2str + "-" + x3str

def elevendigitkey_a():
    def eleven_cd_keygen_first_segment():
        first_segment = str(random.randint(0, 9991)).rjust(4, "0")
        last_digit = int(first_segment[2]) + random.randint(1, 2)

        if last_digit == 10:
           first_segment = str(first_segment[0] + first_segment[1] + first_segment[2] + "0")
        elif last_digit == 11:
            first_segment = str(first_segment[0] + first_segment[1] + first_segment[2] + "1")
        else:
           first_segment = str(first_segment[0] + first_segment[1] + first_segment[2] + str(last_digit))

        return first_segment


    def keygen_seven_digit():
        six_digits = str(random.randint(0, 999999))
        seventh_digit = random.randint(0, 9)
        while seventh_digit == 0 or seventh_digit >= 8:
           seventh_digit = random.randint(0, 9)
        seven_digits = (six_digits + str(seventh_digit)).rjust(7, '0')

        sum = 0
        for x in seven_digits:
           sum += int(x)

        return seven_digits, sum


    def check_seven_digit():
        seven_digits, sum = keygen_seven_digit()
        while sum % 7 != 0:
            seven_digits, sum = keygen_seven_digit()

        return seven_digits

    cd_key_2 = eleven_cd_keygen_first_segment() + '-' + check_seven_digit()
    return cd_key_2
    
def mod7_check(mod7_key, mod7_length):
    total_sum = 0
    for i in range(mod7_length):
        if mod7_key[i].isdigit():
            total_sum = total_sum + int(mod7_key[i])

    valid = total_sum % 7
    if valid == 0:
        return True
    else:
        return False


def retail_key(key):
    const_value = key[0:3]
    if const_value in ['333', '444', '555', '666', '777', '888', '999']:
        return False
    else:
        mod7_key = key[4:15]
        mod7_length = len(mod7_key)
        if mod7_check(mod7_key, mod7_length):
            return True
        else:
            return False

def oem_key(key):
    const1 = key[0:3]
    const2 = key[3:5]
    oem_check = key[6:9]
    mod7_key = key[10:17]

    if oem_check == "OEM":
        if 1 <= int(const1) <= 366:
            if (95 <= int(const2) <= 99) or (0 <= int(const2) <= 2):
                mod7_length = len(mod7_key)
                if mod7_check(mod7_key, mod7_length):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False
        
def validate_elevendigitkey(key):
    segments = key.split('-')
    
    if len(segments) != 2:
        return False
    
    first_segment = segments[0]
    second_segment = segments[1]
    
    if len(first_segment) != 4 or not first_segment.isdigit():
        return False
    
    if len(second_segment) != 7 or not second_segment.isdigit():
        return False
    
    third_digit = int(first_segment[2])
    fourth_digit = int(first_segment[3])
    
    if third_digit == fourth_digit:
        return False
    
    last_digit_first_segment = int(first_segment[3])
    overflow_value = (third_digit + 1) % 10
    overflow_value_alt = (third_digit + 2) % 10
    
    if overflow_value != last_digit_first_segment and overflow_value_alt != last_digit_first_segment:
        return False
    
    return True

    
def verify_mod7(key):
    print(key)
    oem_check = key[6:9]
    
    if retail_key(key) == True and 'OEM' not in key and 'oem' not in key and key[3] == '-':
        print("Valid Retail Key")
    if oem_key(key) == True:
        print("Valid OEM Key")
    if validate_elevendigitkey(key) == True:
        print("Valid NT4/Office 97 key")
    if oem_key(key) == False and retail_key(key) == False:
        print("Invalid key")
    if validate_elevendigitkey(key) == False and oem_key(key) == False and retail_key(key) == False and validate_elevendigitkey(key) == "":
        print("Invalid key")
    else:
        print("Invalid key")

