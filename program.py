import itertools
import json
import common
import time
import os

def print_data_point(data_point, key: str, index: int, ciphers: list[str]) -> None:
    possible_key = key + data_point['word']
    possible_ciphers = ""
    for cipher in ciphers:
        possible_ciphers += f"\n\t-> {common.try_hex_to_string(common.xor_strings(cipher, possible_key))}"
    print(f"{index}. Key: {common.try_hex_to_string(possible_key)}{possible_ciphers}")

def interactive_selection(data, key: str, ciphers: list[str]):
    for index, data_point in enumerate(data, start=1):
        print_data_point(data_point, key, index, ciphers)

def filter_by_position(data, position: int):
    return [item for item in data if item['position'] == position]

if __name__ == "__main__":
    # Load dependencies
    with open(common.CIPHERFILE, 'r', encoding=common.ENCODING) as file:
        ciphers: list[str] = sorted([item.replace("\n", "") for item in file.readlines()], key=len, reverse=True)
    with open(common.WORDFILE, 'r', encoding=common.ENCODING) as file:
        words: list[str] = [item.replace("\n", "") for item in file.readlines()]

    # Calculate target key length
    target_key_len = max([len(item) for item in ciphers])

    c0: str = ciphers[0]
    c1: str = ciphers[1]

    # 1. Guess a word that might appear in one of the messages
    # 2. Encode the word from step 1 to a hex string
    for word_index, word in enumerate([common.string_to_hex(item) for item in words], start=1):
        # 3. XOR the two cipher-text messages
        cx: str = common.xor_strings(c0, c1)
        # 4. XOR the hex string from step 2 at each position of the XOR of the two cipher-texts (from step 3)

        # Attempt to drag the crib across the combined ciphertexts
        for cx_position in range(len(cx) - len(word) + 1):
            segment = cx[cx_position:(cx_position + len(word))]
            result = common.xor_strings(segment, word)
            s = common.try_hex_to_string(result)
            if s and common.is_readable(s):
                print(f"{cx_position}. {s}")

        # 5. When the result from step 4 is readable text, we guess the English word and expand our crib search.
        # 6. If the result is not readable text, we try an XOR of the crib word at the next position.

        quit()



    # Iterate over all (likely) combinations and build a key
    key: str = ""
    while len(key) < target_key_len:
        # Perform crib drag
        for index, word_hex in enumerate([common.string_to_hex(item) for item in words], start=1):
            # Try to decrypt all ciphers
            plaintexts: list[str] = [common.try_hex_to_string(common.xor_strings(cipher, key + word_hex)) for cipher in ciphers]
            # If all ciphers are readable present it to the user
            if all([common.is_readable(plaintext) for plaintext in plaintexts]):
                 # List selection options
                print(f"{index}. {common.try_hex_to_string(word_hex)}")
                for plaintext in plaintexts:
                    print(f"-> {plaintext}")
                # Interactive selection
                while True:
                    try:
                        print()
                        #return data[int(input(f"Select: ")) - 1]
                    except:
                        # Selection failed
                        print(f"User input error! Select between 1 and including {len(data)} (Ctrl + C to quit)")
                        time.sleep(0.5)

        quit()

        # Filter by position
        data_by_pos = filter_by_position(data, len(key))

        # Get all unique words at position
        words: list[str] = list(set([item['word'] for item in data_by_pos]))

        # Filter by word
        data_at_current_pos_by_word = []
        for word in words:
            data_at_current_pos_by_word.append([item for item in data_by_pos if item['word'] == word][0])

        # Filter by if readable
        data_at_current_pos_by_readable_word = []
        for item in data_at_current_pos_by_word:
            if all([common.is_readable(common.xor_strings()) for c in ciphers]):
                data_at_current_pos_by_readable_word.append(item)

        
        if len(data_at_current_pos_by_word) == 0:
            print("Error, no data!")
            quit()
        elif len(data_at_current_pos_by_word) == 1:
            key += data_at_current_pos_by_word[0]['word']
        else:
            key += interactive_selection(data_at_current_pos_by_word, key, ciphers)['word']
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
            except:
              print("Could not clear the terminal")
    
    # Decrypting ciphers
    plaintexts_hex: list[str] = []
    for cipher in ciphers:
        plaintexts_hex.append(common.try_hex_to_string(common.xor_strings(cipher, key)))

    # Collect all results
    result = {
        "ciphertexts": ciphers,
        "plaintexts": plaintexts_hex,
        "key": key
    }

    # Write results to disk
    with open(common.RESULTSFILE, "w") as file:
        json.dump(result, file, indent=common.JSONINDENT)
        print(f"Wrote results to file {common.RESULTSFILE}")

    print("Done! :)")
    quit()