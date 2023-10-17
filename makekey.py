import common
import json
import time
import os

AUTO: bool = False

def interactive_print_data(data_point, key: str, index: int, ciphers: list[str]) -> None:
    possible_key = key + data_point['word']
    possible_ciphers = ""
    for cipher in ciphers:
        possible_ciphers += f"\n\t-> {common.try_hex_to_string(common.xor_strings(cipher, possible_key))}"
    print(f"{index}. Key: {common.try_hex_to_string(possible_key)}{possible_ciphers}")

def interactive_selection(data, key: str, ciphers: list[str]):
    # List selection options
    for index, data_point in enumerate(data, start=1):
        interactive_print_data(data_point, key, index, ciphers)

    # Interactive selection
    while True:
        try:
            return data[int(input(f"Select: ")) - 1]
        except:
            # Selection failed
            print(f"User input error! Select between 1 and including {len(data)} (Ctrl + C to quit)")
            time.sleep(0.5)

# def llm_filter(data, key: str, ciphers: list[str]):
#     for item in data:
#         possible_key = key + item['word']
#         plaintexts = []
#         for cipher in ciphers:
#             decrypted = common.xor_strings(cipher, possible_key)
#             decrypted_str = common.try_hex_to_string(decrypted)
#             plaintexts.append(decrypted_str)
#             item[cipher] = decrypted_str
#         item['ok'] = True if all(llm.could_be_valid_substring(item) for item in plaintexts) else False
#     return [a for a in data if a['ok']]

if __name__ == "__main__":
    # Load data
    print(f"Loading data from file \"{common.CRIBRESULTFILE}\" please wait...")
    with open(common.CRIBRESULTFILE, 'r') as file:
        data = json.load(file)
    
    # Get all ciphers in data set
    ciphers = list(set([item["cipher-1"] for item in data] + [item["cipher-2"] for item in data]))
    print(f"{len(ciphers)} ciphers")

    # Calculate target key length
    target_key_len = max([len(item) for item in ciphers])
    # print(f"The target key length is {target_key_len}")

    # Iterate over all (likely) combinations and build a key
    key: str = ""
    while len(key) < target_key_len:
        data_at_current_pos = [item for item in data if item['position'] == len(key)]

        words: list[str] = list(set([item['word'] for item in data_at_current_pos]))
        data_at_current_pos_by_word = []
        for word in words:
            data_at_current_pos_by_word.append([item for item in data_at_current_pos if item['word'] == word][0])
        
        if len(data_at_current_pos_by_word) == 0:
            print("Error, no data!")
            quit()
        elif len(data_at_current_pos_by_word) == 1:
            key += data_at_current_pos_by_word[0]['word']
        # elif AUTO:
        #     key += interactive_selection(llm_filter(data_at_current_pos_by_word, key, ciphers), key, ciphers)['word']
        else:
            key += interactive_selection(data_at_current_pos_by_word, key, ciphers)['word']
            os.system('cls' if os.name == 'nt' else 'clear')
    
    # Decrypting ciphers
    plaintexts: list[str] = []
    for cipher in ciphers:
        plaintexts.append(common.try_hex_to_string(common.xor_strings(cipher, key)))

    # Collect all results
    result = {
        "ciphertexts": ciphers,
        "plaintexts": plaintexts,
        "key": key
    }

    # Write results to disk
    with open(common.RESULTSFILE, "w") as file:
        json.dump(result, file, indent=common.JSONINDENT)
        print(f"Wrote results to file {common.RESULTSFILE}")

    print("Done! :)")
    quit()