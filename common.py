from typing import Union

CRIBRESULTFILE = "crib-results.json"
CIPHERFILE = "attachment-easy"
WORDFILE = "1000eng.txt"
RESULTSFILE = "results.json"
JSONINDENT = 4
ENCODING = "ASCII"

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
