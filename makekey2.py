import common
import string
import json
import time

def interactive_selection(data):
    # List selection options
    for i, selection_option in enumerate(data, start=1):
        possible = {
            "c1xr-str": ""
            "c1xr-str":
        }
        print(f"{i}. Guess:\t{'_' if selection_option['guess'] == ' ' else selection_option['guess']}\n\tc1xr-str\t{selection_option['c1xr-str']}\n\tc2xr-str\t{selection_option['c2xr-str']}")

    # Interactive selection
    selected = None
    while not selected:
        try:
            selection_input = input(f"Select: ")
            if selection_input.lower() in ['q', 'quit', 'exit']:
                quit()
            selected = data[int(selection_input) - 1]
        except:
            # Selection failed, will let user try again
            print(f"User input error! Select between 1 and including {len(data)} or type 'q' to quit.")
            time.sleep(0.5)  # Otherwise i cannot ctrl + c
    return selected



if __name__ == "__main__":
    print(f"Loading {common.CRIBRESULTFILE}, please wait...")
    with open(common.CRIBRESULTFILE, 'r') as file:
        data = json.load(file)
    
    key_target_length = max(max([len(item['cipher1']) for item in data]), max([len(item['cipher2']) for item in data]))
    print(f"Key target length {key_target_length}")

    key_in_hex: str = ""
    while len(key_in_hex) < key_target_length:
        data_at_pos = [item for item in data if item['position'] == len(key_in_hex)]
        key_in_hex += interactive_selection(data_at_pos)
    
    print(f"Key: {common.hex_to_string(key_in_hex)}")