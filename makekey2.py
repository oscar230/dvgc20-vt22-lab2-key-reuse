import common
import json
import time


def interactive_selection(data, key_hex: str):
    key_ascii = common.hex_to_string(key_hex)

    selected = None
    if len(data) == 0:
        print("Error, no data for this position!")
        quit()
    elif len(data) == 1:
        selected = data[0]
        print(f"One option, automaticly chosen {selected['guess']}")
    else:
        c1 = data[0]['cipher1']
        c2 = data[0]['cipher2']

        # List selection options
        for i, selection_option in enumerate(data, start=1):
            next_key = common.try_hex_to_string(key_hex) + selection_option['guess']
            key_to_print = f"key: {next_key}"

            next_c1xr = selection_option['c1xr-str']
            c1xr_to_print = f"c1xr: {next_c1xr}"

            c2xr = selection_option['c2xr-str']
            c2xr_to_print = f"c2xr: {c2xr}"

            print(f"\n{i}.\t{key_to_print}\n\t{c1xr_to_print}\n\t{c2xr_to_print}")

        # Interactive selection
        current_position: int = list(set([item['position'] for item in data]))[0]
        while not selected:
            try:
                selection_index = input(f"\nCurrent position {current_position}\nSelect: ")
                selected = data[int(selection_index) - 1]
            except:
                # Selection failed
                print(f"User input error! Select between 1 and including {len(data)} (Ctrl + C to quit)")
                time.sleep(0.5)
    
    return selected



if __name__ == "__main__":
    print(f"Loading {common.CRIBRESULTFILE}, please wait...")
    with open(common.CRIBRESULTFILE, 'r') as file:
        data = json.load(file)
    
    key_target_length = max(max([len(item['cipher1']) for item in data]), max([len(item['cipher2']) for item in data]))
    print(f"Key target length {key_target_length}")

    key_hex: str = ""
    while len(key_hex) < key_target_length:
        data_at_pos = [item for item in data if item['position'] == len(key_hex)]
        key_hex += interactive_selection(data_at_pos, key_hex)['drag-result']
    
    print(f"\nDone!\nKey hex: {key_hex}\nKey str: {common.hex_to_string(key_hex)}")