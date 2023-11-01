import common
from typing import Union
from pick import pick

class KeyPart:
    position: int # Position in the hex string
    key_part: str # Represented as a hex string

    def __init__(self, position: int, key_part: str) -> None:
        self.position = position
        self.key_part = key_part

    def end_position(self) -> int:
        return self.position + len(self.key_part) - 1
    
class Word:
    word: str

    def __init__(self, word_as_string: str) -> None:
        self.word = common.string_to_hex(word_as_string)

    def __str__(self):
     return common.hex_to_string(self.word)
        
class Cipher:
    cipher: str

    def __init__(self, cipher: str) -> None:
        self.cipher = cipher

    def to_plaintext(self, key_parts: list[KeyPart], key_len: int) -> str:
        # Build key
        key: str = build_key(key_parts, key_len)
        
        # print(f"Key      {key} ({common.try_hex_to_string(key)})")
        # print(f"Cipher   {self.cipher}")

        plaintext: str = ""
        for i in range(0, len(key), 2):
            if self.cipher[i:i+2] == common.PADDING_CHAR or key[i:i+2] == common.PADDING_CHAR:
                # Current character is a placeholder character
                # Should be represented by another character
                plaintext += common.PADDING_DISPLAY_CHAR
            else:
                new_char: str = common.xor_strings(self.cipher[i:i+2], key[i:i+2])

                if common.is_readable(new_char):
                    # Current character is readable
                    # Should be added to key
                    plaintext += new_char
                else:
                    # Current character cannot be read
                    plaintext += common.PADDING_DISPLAY_CHAR
            
            # print(f"pos={i}\t{self.cipher[i:i+2]} ^ {key[i:i+2]} = {common.xor_strings(self.cipher[i:i+2], key[i:i+2])} ==> {plaintext}")
        return plaintext

def build_key(key_parts: list[KeyPart], key_len: int) -> str:
    key: str = "" # Hex
    for i in range(0, key_len + 2, 2): # Skip every other becouse of hex being represenated as a string
        if len(key) < i:
            if any([a for a in key_parts if a.position == i]):
                key += [a for a in key_parts if a.position == i][0].key_part
            else:
                key += common.PADDING_CHAR
    return key

def load_words() -> list[Word]:
    with open(common.WORDFILE, 'r', encoding = common.ENCODING) as file:
        words: list[str] = [item.replace("\n", "") for item in file.readlines()]
        return [Word(word) for word in words]

def load_ciphers() -> tuple[list[Cipher], int]:
    with open(common.CIPHERFILE, 'r', encoding = common.ENCODING) as file:
        ciphers: list[str] = [item.replace("\n", "") for item in file.readlines()]
        ciphers = sorted(ciphers, key=len, reverse=True)
        return [Cipher(item) for item in ciphers], len(ciphers[0])

def pick_position(word: Word, cipher_x: Cipher, key_parts: list[KeyPart]) -> Union[KeyPart, None]:
    pick_options: list = []
    pick_options.append("## done ##")
    new_key_parts: list[KeyPart] = []
    for curr_pos in range(0, len(cipher_x.cipher) - len(word.word) + 1, 2):
        current_key_parts: list[KeyPart] = list(key_parts)

        new_key_part: KeyPart = KeyPart(curr_pos, word.word)
        new_key_parts.append(new_key_part)
        current_key_parts.append(new_key_part)

        plaintext: str = cipher_x.to_plaintext(current_key_parts, key_len)
        
        # print("cipher x\tkey\tplaintext")
        # print(f"{cipher_x.cipher} ^ key = {plaintext} = {common.try_hex_to_string(plaintext)}")
        
        # Eeeh!
        e: str = ""
        f = common.try_hex_to_string(plaintext)
        if f:
            e = f

        pick_options.append(f'{curr_pos}\t{e} ({plaintext})')
    _, index = pick(pick_options, f'Select position for word \"{word}\".')
    if index == 0:
        return None
    else:
        return new_key_parts[index - 1]

def pick_word(words: list[Word]) -> Union[KeyPart, None]:
    pick_options: list = []
    pick_options.append("## done ##")
    for word in words:
        pick_options.append(f"{word}")
    _, index = pick(pick_options, f'Select a word to drag.')
    if index == 0:
        return None
    else:
        return words[index - 1]

if __name__ == "__main__":
    ciphers: list[Cipher]
    key_len: int
    ciphers, key_len = load_ciphers()
    words: list[Word] = load_words()

    key_parts: list[KeyPart] = []

    # XOR the two longest ciphers
    cipher_x: Cipher = Cipher(common.xor_strings(ciphers[0].cipher, ciphers[1].cipher))

    done: bool = False
    while not done:
        word: Union[Word, None] = pick_word(words)
        if word:
            new_key_part: Union[KeyPart, None] = pick_position(word, cipher_x, key_parts)
            if new_key_part:
                key_parts.append(new_key_part)
            else:
                done = True
        else:
            done = True
    
    print(f"Done :)\nKey\t{build_key(key_parts, key_len)}")