import common
import string
import json
import time

def interactive_selection(select_from: list[str]) -> str:
    # List cribs
    for i, selection_option in enumerate(select_from, start=1):
        print(f"{i}. {'_' if selection_option == ' ' else selection_option}")

    # Interactive selection
    while True:
        try:
            selection_input = input(f"Select: ")
            if selection_input.lower() in ['q', 'quit', 'exit']:
                quit()
            selected = select_from[int(selection_input) - 1]
            return selected
        except:
            # Selection failed, will let user try again
            print(f"User input error! Select between 1 and including {len(select_from)} or type 'q' to quit.")
            time.sleep(0.5)  # Otherwise i cannot ctrl + c


if __name__ == "__main__":
    print(f"Loading {common.CRIBRESULTFILE}, please wait...")
    with open(common.CRIBRESULTFILE, 'r') as file:
        data = json.load(file)
    
    key_target_length = max(max([len(item['cipher1']) for item in data]), max([len(item['cipher2']) for item in data]))
    print(f"Key target length {key_target_length}")

    key_in_hex: str = ""
    while len(key_in_hex) < key_target_length:
        interactive_selection()