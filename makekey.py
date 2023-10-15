import json
from typing import Union, Set
import llm
import time
import common
import string
from collections import defaultdict

AUTO: bool = True

def predict_crib(key: str, cribs: list[str]) -> str:
    prediction = llm.predict(key, cribs)
    sorted_predictions = sorted(prediction.items(), key=lambda x: x[1])
    for s in sorted_predictions:
        print(s)
    return sorted_predictions[0][0]

def select_crib(key: str, cribs: list[str]):
    if len(key) > 0 and key[-1] != ' ' and ' ' in cribs:
        print("Space added.")
        return ' '
    else:
        if AUTO and len(key) > 0:
            # Make prediction using LLM
            return predict_crib(key, cribs)
        else:
            # Display user interaction
            return interactive_selection(cribs)

def interactive_selection(cribs: list[str]) -> str:
    # List cribs
    for i, crib in enumerate(cribs, start=1):
        s = f"{i}. {key}"
        s += "_" if crib == ' ' else crib
        print(s)
    # Interactive selection
    while True:
        try:
            selection_input = input(f"Select crib: ")
            if selection_input.lower() in ['q', 'quit', 'exit']:
                quit()
            selected_crib = cribs[int(selection_input) - 1]
            return selected_crib
        except:
            # Selection failed, will let user try again
            print(f"User input error! Select between 1 and including {len(cribs)} or type 'q' to quit.")
            time.sleep(0.5)  # Otherwise i cannot ctrl + c


def is_human_readable(text) -> bool:
    # return len(text) == sum(1 for char in text if char.isalpha() or char.isspace())
    human_readable_chars = string.printable[:-5]
    return all(char in human_readable_chars for char in text)

if __name__ == "__main__":
    print(f"Loading {common.CRIBRESULTFILE}, please wait...")
    with open(common.CRIBRESULTFILE, 'r') as file:
        data = json.load(file)

    key_target_length = max(max([len(item['c1']) for item in data]), max([len(item['c2']) for item in data]))
    print(f"Key target length {key_target_length}")

    key: str = ""
    while len(key) < key_target_length:
        position = len(common.string_to_hex(key))
        ciphers = list(set([item['c1'] for item in data] + [item['c2'] for item in data if item['position'] == position]))
        cribs = list(set([item['result'] for item in data if item['position'] == position]))
        words = list(set([item['word'] for item in data if item['position'] == position]))

        print(f"Position {position}")
        print(f"\t{len(ciphers)} ciphers")
        print(f"\t{len(cribs)} cribs")
        print(f"\t{len(words)} words")

        possible_key_parts = []
        for crib in cribs:
            for cipher in ciphers:
                xor = common.xor_strings(crib, cipher)
                possible_key_part = {
                    "cipher": cipher,
                    "crib": crib,
                    "crib_as_string": common.try_hex_to_string(crib),
                    "xor_as_string": common.try_hex_to_string(xor)
                }
                possible_key_parts.append(possible_key_part)

        # Filter for human readable text
        possible_key_parts = [item for item in possible_key_parts if item['xor_as_string'] and is_human_readable(item['xor_as_string'])]

        # Filter for cribs that do work on all ciphers
        cipher_to_cribs = defaultdict(set)
        for item in possible_key_parts:
            if "cipher" in item and "crib" in item:
                cipher_to_cribs[item["cipher"]].add(item["crib"]) # For each cipher collect it's associated crib
        common_cribs = set.intersection(*cipher_to_cribs.values()) # Get common cribs across ciphers
        possible_key_parts = [item for item in possible_key_parts if item["crib"] in common_cribs] # Filter by common cribs

        #
        #   Make selection
        #
        selection = interactive_selection([item['xor_as_string'] for item in possible_key_parts])
        r = []
        r.append([item['word'] for item in data])

        #
        #   Write results to disk
        #
        with open('a.json', "w") as file:
            json.dump(r, file, indent=common.JSONINDENT)
            print(f"Wrote results to file {common.CRIBRESULTFILE}")


        quit()

    quit()
    if data:
        key: str = ""
        next_sub_key: Union[str, None] = "#"

        while next_sub_key:
            # Get cribs avaliable at the key's current postition
            position = len(common.string_to_hex(key))
            avaliable_cribs = get_at_position(data, position)
            if not avaliable_cribs:
                # There are no cribs avaliable at this postition, the crib drag might be completed or this is an unexpected error
                print("No cribs avaliable")
                next_sub_key = None
            else:
                # There are cribs avaliable, make a selection
                next_sub_key = select_crib(key, avaliable_cribs)
                key += next_sub_key
            print(f"Key:{key} ({common.string_to_hex(key)})")

        with open(common.CIPHERFILE, 'r') as file:
            for cipher in [item.replace("\n", "") for item in file.readlines()]:
                print(f"{cipher} -> {common.xor_strings(cipher, common.string_to_hex(key))}")

        print(f"Done")
        quit()