from typing import Union

CRIBRESULTFILE = "crib-results.json"
CIPHERFILE = "attachment-easy"
WORDFILE = "wordlist"
RESULTSFILE = "results.json"
JSONINDENT = 4
ENCODING = "ASCII"
PADDING_CHAR: str = '00' # This is the NULL character in the ASCII char set
PADDING_DISPLAY_CHAR: str = '5f' # This is a underscore
# UNREADABLE_REPLACEMENT_CHAR_DISPLAY: str = '7e' # This is... this ~

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

def readable_char_set() -> str:
    return 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .123456789'

def is_readable(input_hex: str) -> bool:
    if input_hex:
        input_str: Union[None, str] = try_hex_to_string(input_hex)
        if input_str:
            return all(char in readable_char_set() for char in input_str)
    return False