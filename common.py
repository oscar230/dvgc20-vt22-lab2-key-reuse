from typing import Union
import re

CRIBRESULTFILE = "crib-results.json"
CIPHERFILE = "attachment-easy"
WORDFILE = "wordlist"
RESULTSFILE = "results.json"
JSONINDENT = 4
ENCODING = "ASCII"

def is_readable(text: str) -> bool:
    # Count of allowed characters
    allowed_count = len(re.findall(r'[A-Za-z0-9 ,."]', text))
    # If more than a certain percentage of the characters are readable
    return allowed_count / len(text) > 0.9
# def is_readable(text: str) -> bool:
#     readable_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '#"!#$%&\'*+,-./?@\\^_`\n\r'
#     return all(char in readable_chars for char in text)
    # pattern = re.compile("^[a-zA-Z0-9?><;,{}[\]\-_+=!@#$%\^&*|']*$")
    # return bool(re.match(pattern, text))

def xor_strings(hex1, hex2):
    # XOR two HEX strings
    return ''.join([f"{(int(a, 16) ^ int(b, 16)):x}" for a, b in zip(hex1, hex2)])

def string_to_hex(s: str) -> str:
    return s.encode().hex()

def hex_to_string(h: str) -> str:
    return bytes.fromhex(h).decode(encoding=ENCODING)

def try_hex_to_string(h: str) -> Union[str, None]:
    result: Union[str, None] = None
    try:
        result = bytes.fromhex(h).decode(encoding=ENCODING)
    except:
        result = None
    finally:
        return result
