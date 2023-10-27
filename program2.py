import common
from typing import Union
import itertools

PLACEHOLDERCHAR: str = common.hex_to_string("00")

def readable() -> str:
    return 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .123456789'

def is_readable(input: str) -> bool:
    return all(char in readable() for char in input)

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
            key += common.string_to_hex(PLACEHOLDERCHAR)
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
        words: list[str] = [item.replace("\n", "") for item in file.readlines()][:10]

    # In preperation, hex all the words from the wordlist
    # It is easier to keep track of data when it is all in the same format (hex)
    words = [common.string_to_hex(word) for word in words]
    
    # Print the characters that are deemed readable
    print(f"Readable chars: \"{readable()}\"")

    # Sort ciphers from longest to shortest
    ciphers = sorted(ciphers, key=len, reverse=True)

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

        avaliable_for_selections = []

        # 4. XOR the hex string from step 2 at each position of the XOR of the two cipher-texts (from step 3)
        for pos in range(len(cipher_x) - len(word) + 1):
            # Drag the crib/word to get the possible key
            # possible_key: str = common.xor_strings(cipher_x[pos:pos+len(word)], word)
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
                # plaintexts: list[str] = [common.xor_strings(possible_key, cipher[pos:len(word)]) for cipher in ciphers]
                plaintexts: list[str] = [build_cipher(c, possible_key_parts, key_len) for c in ciphers]

                # 6. If the result is not readable text, we try an XOR of the crib word at the next position.
                # Convert all plaintexts (hex) to readable string, None means it could not be converted (bad format)
                plaintexts_str: list[Union[None, str]] = [common.try_hex_to_string(item) for item in plaintexts]
                
                if all([item and is_readable(item) for item in plaintexts_str]):
                    # Store for later selection by user
                    avaliable_for_selections.append({
                        "pos": pos,
                        "plaintexts": plaintexts_str
                    })

        if len(avaliable_for_selections) > 0:
            # Print the guessed word
            print(f"Guessed word: {word_str}")
            
            # Print options for user
            for a in avaliable_for_selections:
                for b in a['plaintexts']:
                    print(f"{a['pos']}.\t{b}")

            # Let the user select
            selection: str = input(f"Type a comma seperated list of positions, to select the word {word_str} at those position, or \"d\" to discard the word and go to next in the wordlist, or \"q\" to quit the program.")
            if (selection == 'd'):
                print(f"Skipping word {word_str}")
            elif (selection == 'q'):
                print("Quit!")
                quit()
            else:
                try:
                    selected_positions: list[int] = [int(item) for item in selection.split(',')]
                except:
                    print("An exception occurred")
                    quit()
                
                print(common.try_hex_to_string(build_key(key_parts, key_len)))
                for selected_pos in selected_positions:
                    key_parts.append({
                        "pos": selected_pos,
                        "key": word
                    })
                    print(f"Added {word_str} at position {selected_pos}")
                    built_key: str = build_key(key_parts, key_len)
                    print(f"{common.try_hex_to_string(built_key)} (0x{built_key})")

        if build_key_len(key_parts) >= key_len:
            print("Done!")
            quit()
            