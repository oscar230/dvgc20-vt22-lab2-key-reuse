from __future__ import annotations
import common
from typing import Union
import inquirer

class KeyPart:
    position: int # Position in the hex string
    key_part: str # Represented as a hex string

    def __init__(self, position: int, key_part: str) -> None:
        self.position = position
        self.key_part = key_part

    def last_position(self) -> int:
        return self.position + len(self.key_part) - 1
    
    def get_char(self, position: int) -> Union[str, None]:
        try:
            x: int = position - self.position
            return self.key_part[x:x+2]
        except:
            return None

    def overlaps_with(self, other: 'KeyPart') -> bool:
        # Check if there is any overlap between this KeyPart and another KeyPart
        return not (self.last_position() < other.position or self.position > other.last_position())

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
        print(f"Cannot decrypt cipher if key is not of the same size as the cipher!\nCipher\t{self.cipher}\nKey\t{key}")
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
            self.key_len = len(self.cipher_x.cipher)
            self.ciphers = [Cipher(item) for item in ciphers]
            self.key_parts = []

    def add_key_part(self, key_part: KeyPart) -> bool:
        if self.does_key_part_fit(key_part):
            self.key_parts.append(key_part)
            return True
        else:
            return False
    
    def does_key_part_fit(self, key_part: KeyPart) -> bool:
        return not any([item.overlaps_with(key_part) for item in self.key_parts])

    def build_key(self, additional_key_part: Union[KeyPart, None]) -> str:
        # Create a copy of the current key parts
        key_parts: list[KeyPart] = list(self.key_parts)
        # This is the key that will be built upon, all starts out as padding characters and will then be replaced
        key: str = common.PADDING_CHAR * int(self.key_len / 2)

        # if an additional key part has been provided, append it to the current key parts
        if additional_key_part:
            key_parts.append(additional_key_part)

        # Itterate over key part
        for key_part in key_parts:
            # Replace the padded characters with the key_parts
            # This assumes that there are no overlapping key parts
            key = key[:key_part.position] + key_part.key_part + key[key_part.last_position() + 1:]

        # Return the final key
        return key

    def is_complete(self) -> bool:
        return not common.PADDING_CHAR in self.build_key(None)

def load_words() -> list[Word]:
    with open(common.WORDFILE, 'r', encoding = common.ENCODING) as file:
        words: list[str] = [item.replace("\n", "") for item in file.readlines()]
        return [Word(word) for word in words]

def pick_position(keyring: Keyring, word: Word) -> Union[KeyPart, None]:
    # Prepare list for valid possible keys
    valid_possible_keys: list = []

    # Add options for each valid position
    for curr_pos in range(0, keyring.key_len - len(word.word) + 2, 2):
        possible_key_part: KeyPart = KeyPart(curr_pos, word.word)

        if keyring.does_key_part_fit(possible_key_part):
            possible_key: str = keyring.build_key(possible_key_part)

            plaintext_display_hex: str = keyring.cipher_x.decrypt_display(possible_key)
            plaintext_display_str: str = common.hex_to_string(plaintext_display_hex)
            plaintext_hex: str = keyring.cipher_x.decrypt(possible_key)

            valid_possible_keys.append({
                "key_part": possible_key_part,
                "text": f'{curr_pos}\t{plaintext_display_str}'#+' {keyring.cipher_x.cipher} ^ {possible_key} = {plaintext_hex}'
            })

    # Prepare options and add valid possible keys
    go_back_text: str = "⬅️  Go back"
    inquirer_options = [
        inquirer.List(
            "valid_possible_key",
            message=f"Choose a position for \"{word}\"",
            choices=[go_back_text] + [item["text"] for item in valid_possible_keys],
        )
    ]

    # Promt for an answer
    answer = inquirer.prompt(inquirer_options)['valid_possible_key']
    if answer == go_back_text:
        return None
    else:
        return [item for item in valid_possible_keys if item['text'] == answer][0]

def pick_word(words: list[Word]) -> Union[Word, None]:
    # Prepare option and add options for each valid position
    done_text: str = "👍 Done"
    inquirer_options = [
        inquirer.List(
            "word",
            message="Choose a word",
            choices=[done_text] + [f'{word}' for word in words],
        )
    ]

    # Promt for an answer    
    answer = inquirer.prompt(inquirer_options)['word']

    if answer == done_text:
        # Quit command
        return None
    else:
        # Return the answer's word
        return [word for word in words if f'{word}' == answer][0]

if __name__ == "__main__":
    words: list[Word] = load_words()
    keyring: Keyring = Keyring()

    done: bool = False
    while not (keyring.is_complete() or done):
        word: Union[Word, None] = pick_word(words)
        if word:
            new_key_part: Union[KeyPart, None] = pick_position(keyring, word)
            if new_key_part:
                keyring.add_key_part(new_key_part)
        else:
            done = True
    
    key: str = keyring.build_key(None)
    print(f"Done! 🎉\nKey\t{key}")
    print(common.try_hex_to_string(key))