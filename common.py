from typing import Union
import hexconverter

CRIBRESULTFILE = "crib-results.json"
CIPHERFILE = "attachment"
WORDFILE = "wordlist"
RESULTSFILE = "results.json"
JSONINDENT = 4
ENCODING = "ASCII"
PADDING_CHAR: str = '00' # This is the NULL character in the ASCII char set
PADDING_DISPLAY_CHAR: str = '5f' # This is a underscore
UNREADABLE_DISPLAY_CHAR: str = '7e' # This is... this ~



def readable_char_set() -> str:
    return 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .123456789'

def is_readable(input_hex: str) -> bool:
    if input_hex:
        input_str: Union[None, str] = hexconverter.try_hex_to_string(input_hex)
        if input_str:
            return all(char in readable_char_set() for char in input_str)
    return False