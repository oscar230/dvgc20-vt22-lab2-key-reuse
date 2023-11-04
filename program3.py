import common
from typing import Union
from pick import pick

class KeyPart:
    position: int # Position in the hex string
    key_part: str # Represented as a hex string

    def __init__(self, position: int, key_part: str) -> None:
        self.position = position
        self.key_part = key_part

    def last_position(self) -> int:
        return self.position + len(self.key_part) - 1
    
    def is_in_range(self, position: int) -> bool:
        return self.position >= position and self.last_position() <= position
    
    def get_char(self, position: int) -> str:
        x: int = position - self.position
        return self.key_part[x:x+2]

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

    def decrypt(self, key: str) -> str:
        return common.xor_strings(self.cipher, key)

    def decrypt_display(self, key: str) -> str:
        if len(key) == len(self.cipher):
            plaintext: str = ''
            for i in range(0, len(self.cipher), 2):
                if key[i:i+2] == common.PADDING_CHAR:
                    # Should be represented by another character than the padding character
                    plaintext += common.PADDING_DISPLAY_CHAR
                else:
                    decrypted_char_at_i: str = common.xor_strings(self.cipher[i:i+2], key[i:i+2])
                    if common.is_readable(decrypted_char_at_i):
                        plaintext += decrypted_char_at_i
                    else:
                        # Current character cannot be read, represent with something else
                        plaintext += common.UNREADABLE_DISPLAY_CHAR
            return plaintext
        print("Cannot decrypt cipher if key is not of the same size as the cipher!")
        quit()

class Keyring:
    ciphers: list[Cipher]
    cipher_x: Cipher
    key_parts: list[KeyPart]
    key_len: int

    def __init__(self) -> None:
        with open(common.CIPHERFILE, 'r', encoding = common.ENCODING) as file:
            ciphers: list[str] = [item.replace("\n", "") for item in file.readlines()]
            ciphers = sorted(ciphers, key=len, reverse=True)
            self.cipher_x = Cipher(common.xor_strings(ciphers[0], ciphers[1]))
            self.key_len = len(ciphers[0])
            self.ciphers = [Cipher(item) for item in ciphers]
            self.key_parts = []

    def add_key_part(self, key_part: KeyPart) -> bool:
        if self.does_key_part_fit(key_part):
            self.key_parts.append(key_part)
            return True
        else:
            return False
    
    def does_key_part_fit(self, key_part: KeyPart) -> bool:
        if key_part.last_position() > self.key_len - 1:
            return False
        for i in range(key_part.position, key_part.last_position() + 1, 2):
            if any(item for item in self.key_parts if item.is_in_range(i)):
                return True
        return False

    def build_key(self, additional_key_part: Union[KeyPart, None]) -> str:
        key_parts: list[KeyPart] = list(self.key_parts)
        key: str = ''
        if additional_key_part:
            key_parts.append(additional_key_part)
        for i in range(0, self.key_len, 2):
            if any([a for a in key_parts if a.is_in_range(i)]):
                curr_key_part: KeyPart = [a for a in key_parts if a.is_in_range(i)][0]
                key += curr_key_part.get_char(i)
            else:
                key += common.PADDING_CHAR
        return key

def load_words() -> list[Word]:
    with open(common.WORDFILE, 'r', encoding = common.ENCODING) as file:
        words: list[str] = [item.replace("\n", "") for item in file.readlines()]
        return [Word(word) for word in words]

def pick_position(keyring: Keyring, word: Word) -> Union[KeyPart, None]:
    pick_options: list = []
    pick_options.append("> Go back")
    for curr_pos in range(0, keyring.key_len - len(word.word) + 2, 2):
        possible_key_part: KeyPart = KeyPart(curr_pos, word.word)
        possible_key: str = keyring.build_key(possible_key_part)

        plaintext_display_hex: str = keyring.cipher_x.decrypt_display(possible_key)
        plaintext_display_str: str = common.hex_to_string(plaintext_display_hex)
        plaintext_hex: str = keyring.cipher_x.decrypt(possible_key)

        pick_options.append(f'{curr_pos}\t{plaintext_display_str} {keyring.cipher_x.cipher} ^ {possible_key} = {plaintext_hex}')
    _, index = pick(pick_options, f'Select position for word \"{word}\" (base key \"{keyring.build_key(None)})\".\n- \"{common.hex_to_string(common.PADDING_DISPLAY_CHAR)}\" are padding since the key is not yet complete.\n- \"{common.hex_to_string(common.UNREADABLE_DISPLAY_CHAR)}\" are unreadable characters.\n- Columns: position, plaintext string, cipher 1 and 2 xored ^ possible key = plaintext hex')
    if index == 0:
        return None
    else:
        return KeyPart(index - 1, word.word)

def pick_word(words: list[Word]) -> Union[Word, None]:
    pick_options: list = []
    pick_options.append("> Done")
    for word in words:
        pick_options.append(f"{word}")
    _, index = pick(pick_options, f'Select a word to drag.')
    if index == 0:
        return None
    else:
        return words[index - 1]

if __name__ == "__main__":
    words: list[Word] = load_words()
    keyring: Keyring = Keyring()

    done: bool = False
    while not done:
        word: Union[Word, None] = pick_word(words)
        if word:
            new_key_part: Union[KeyPart, None] = pick_position(keyring, word)
            if new_key_part:
                keyring.add_key_part(new_key_part)
        else:
            done = True
    
    print(f"Done!\nKey\t{keyring.build_key(None)}")