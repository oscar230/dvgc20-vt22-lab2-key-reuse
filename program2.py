import common
from typing import Union
import itertools
import os

PLACEHOLDERCHAR: str = "23" # As hex

def readable() -> str:
    return 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .123456789'

def is_readable(input: Union[str, None]) -> bool:
    if input:
        input = input.replace(common.hex_to_string(PLACEHOLDERCHAR), '')
        return all(char in readable() for char in input)
    else:
        return False

def crib_drag(ciphertexts_xored: str, crib: str) -> list[str]:
    results = []
    for i in range(len(ciphertexts_xored) - len(crib) + 1):
        segment = ciphertexts_xored[i:i+len(crib)]
        result = common.xor_strings(segment, crib)
        results.append((i, result))
    return results

def build_key(key_parts: list, length: int) -> str:
    key: str = ""
    for i in range(0, length):
        keys_at_pos: list = [item for item in key_parts if item['pos'] <= i and item['pos'] + len(item['key']) - 1 >= i]
        if not keys_at_pos:
            key += PLACEHOLDERCHAR
        elif len(keys_at_pos) == 1:
            key += keys_at_pos[0]['key'][i - keys_at_pos[0]['pos']]
        else:
            print("Build key error, overlapping key parts!")
            print(keys_at_pos)
            quit()
    return key

def build_key_len(key_parts: list) -> int:
    return sum([len(item['key']) + item['pos'] for item in key_parts])

def build_cipher(cipher: str, key_parts: list, key_len: int) -> str:
    return common.xor_strings(cipher, build_key(key_parts, key_len))

def is_overlapping(key_parts: list) -> bool:
    for (a, b) in itertools.combinations(key_parts, 2):
        pos_a = a["pos"]
        pos_b = b["pos"]
        
        end_pos_a = pos_a + len(a["key"])
        end_pos_b = pos_b + len(b["key"])

        if (pos_a <= end_pos_b and end_pos_b <= end_pos_a) or (pos_b <= end_pos_a and end_pos_a <= end_pos_b):
            return True
    return False

if __name__ == "__main__":
    # Load ciphers
    with open(common.CIPHERFILE, 'r', encoding=common.ENCODING) as file:
        ciphers: list[str] = sorted([item.replace("\n", "") for item in file.readlines()], key=len, reverse=True)
    
    # Load word list
    with open(common.WORDFILE, 'r', encoding=common.ENCODING) as file:
        words: list[str] = [item.replace("\n", "") for item in file.readlines()][:20]

    # In preperation, hex all the words from the wordlist
    # It is easier to keep track of data when it is all in the same format (hex)
    words = [common.string_to_hex(word) for word in words]
    
    # Print number of words
    print(f"{len(words)} words")

    # Print the characters that are deemed readable
    print(f"Readable chars: \"{readable()}\"")

    # Sort ciphers from longest to shortest
    ciphers = sorted(ciphers, key=len, reverse=True)

    # Print number of ciphers
    print(f"{len(ciphers)} ciphertexts")

    # Calculate target key length
    # key_len: int = max([len(item) for item in ciphers])
    key_len: int = len(ciphers[0])
    print(f"Key length: {key_len}")

    # Partial decryption key in hex
    key_parts: list = []

    # XOR the two longest ciphers
    cipher_x: str = common.xor_strings(ciphers[0], ciphers[1])

    # From: https://crypto.stackexchange.com/a/10163
    # 1. Guess a word that might appear in one of the messages
    # 2. Encode the word from step 1 to a hex string
    # 3. XOR the two cipher-text messages
    for word in words:
        word_str = common.hex_to_string(word)

        drags = []

        # 4. XOR the hex string from step 2 at each position of the XOR of the two cipher-texts (from step 3)
        for pos in range(0, len(cipher_x) - len(word) + 1, 2): # Use a step of 2 since HEX takes up 2 characters when represented as a string
            # Apply the new possible word (crib) to a new theoretical key
            possible_key_parts: list = list(key_parts) # copy list
            possible_key_parts.append({
                "pos": pos,
                "key": word
            })

            if is_overlapping(possible_key_parts):
                # Check if new key part overlapps
                print(f"Cannot use {word_str} at position {pos}, it is overlapping!")
            else:
                # 5. When the result from step 4 is readable text, we guess the English word and expand our crib search.
                # Use the possible key to try and decrypt all ciphertexts
                plaintexts: list[str] = [build_cipher(cipher, possible_key_parts, key_len) for cipher in ciphers]

                # Store for later selection by user
                drags.append({
                    "pos": pos,
                    "plaintexts": plaintexts
                })

        # If there are no dragged cribs to select from then there is nothing to do
        if len(drags) > 0:

            # Print options for user
            print(f"Pos.\tplaintext")
            for drag in drags:
                for plaintext in drag['plaintexts']:
                    print(f"{drag['pos']}\t{common.try_hex_to_string(plaintext)}\t({plaintext})")

            # Print the guessed word
            print(f"Guessed word: {word_str}")

            # Let the user select
            selection: str = input(f"Type positions (seperated by comman), \"d\" to discard or \"q\" to quit: ")
            if (selection == 'd'):
                print(f"Skipping word {word_str}")
            elif (selection == 'q'):
                print("Quit!")
                quit()
            else:
                try:
                    selections: list[int] = [int(item) for item in selection.split(',')]
                except:
                    print("An exception occurred")
                    quit()
                
                # Clear the terminal
                os.system('cls' if os.name == 'nt' else 'clear')

                print(common.try_hex_to_string(build_key(key_parts, key_len)))
                for selection in selections:
                    if not selection % 2 == 0:
                        print("Number must be event!")
                        quit()
                    else:
                        key_parts.append({
                            "pos": selection,
                            "key": word
                        })
                        print(f"Added {word_str} at position {selection}")
                        built_key: str = build_key(key_parts, key_len)
                        print(f"{common.try_hex_to_string(built_key)} (0x{built_key})")

        # If the key is of sufficient length then we are done
        if build_key_len(key_parts) >= key_len:
            print("Done!")
            quit()
            
    print("No more words!")
    quit()