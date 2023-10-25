import common
from typing import Union

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

if __name__ == "__main__":
    # Load ciphers
    with open(common.CIPHERFILE, 'r', encoding=common.ENCODING) as file:
        ciphers: list[str] = sorted([item.replace("\n", "") for item in file.readlines()], key=len, reverse=True)
    
    # Load word list
    with open(common.WORDFILE, 'r', encoding=common.ENCODING) as file:
        words: list[str] = [item.replace("\n", "") for item in file.readlines()][:3]

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
    key: str = '_' * key_len


    # XOR the two longest ciphers
    cipher_x: str = common.xor_strings(ciphers[0], ciphers[1])

    # From: https://crypto.stackexchange.com/a/10163
    # 1. Guess a word that might appear in one of the messages
    # 2. Encode the word from step 1 to a hex string
    # 3. XOR the two cipher-text messages
    for word in words:
        word_str = common.hex_to_string(word)
        # Print the guessed word
        print(f"Guessed word: {word_str}")

        # 4. XOR the hex string from step 2 at each position of the XOR of the two cipher-texts (from step 3)
        for pos in range(len(cipher_x) - len(word) + 1):
            # Drag the crib/word to get the possible key
            possible_key: str = common.xor_strings(cipher_x[pos:pos+len(word)], word)

            # 5. When the result from step 4 is readable text, we guess the English word and expand our crib search.
            # Use the possible key to try and decrypt all ciphertexts
            plaintexts: list[str] = [common.xor_strings(possible_key, cipher[pos:len(word)]) for cipher in ciphers]

            # 6. If the result is not readable text, we try an XOR of the crib word at the next position.
            # Convert all plaintexts (hex) to readable string, None means it could not be converted (bad format)
            plaintexts_str: list[Union[None, str]] = [common.try_hex_to_string(item) for item in plaintexts]

            if all([item and is_readable(item) for item in plaintexts_str]):
                # Print the current position
                print(f"\tAt position: {pos}")

                # Print all possible plaintexts from this word
                for item in plaintexts_str:
                    print(f"\t\tPlaintext: {item}")

        selection: str = input(f"Type a comma seperated list of positions, to select the word {word_str} at those position, or \"d\" to discard the word and go to next in the wordlist, or \"q\" to quit the program.")
        if (selection == 'd'):
            print("Next word :)")
        elif (selection == 'q'):
            print("Quit!")
            quit()
        else:
            try:
                selected_positions: list[int] = [int(item) for item in selection.split(',')]
            except:
              print('An exception occurred')
              quit()
            
            print(key)
            for selected_pos in selected_positions:
                pre_key: str = key[0:selected_pos]
                new_key: str = word
                post_key: str = key[len(word):len(key)]
                key = pre_key + new_key + post_key
                print(key)
            