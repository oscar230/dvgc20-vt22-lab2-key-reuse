from typing import Union
import common

def string_to_hex(s: str) -> str:
    return s.encode().hex()

def hex_to_string(h: str) -> str:
    return bytes.fromhex(h).decode(encoding=common.ENCODING)

def try_hex_to_string(h: str) -> Union[str, None]:
    result: Union[str, None] = None
    try:
        result = bytes.fromhex(h).decode(encoding=common.ENCODING)
    except:
        result = None
    finally:
        return result