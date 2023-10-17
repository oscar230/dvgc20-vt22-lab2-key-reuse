import common
import json
import time

def interactive_print_data(data_point, key: str, index: int, ciphers: list[str]) -> None:
    p_key = key + data_point['word']
    p_c = ""
    for cipher in ciphers:
        p_c += f"\n\t-> {common.try_hex_to_string(common.xor_strings(cipher, p_key))}"
    print(f"{index}. Key: {common.try_hex_to_string(p_key)}{p_c}")

def interactive_selection(data, key: str, ciphers: list[str]):
    if len(data) == 0:
        print("Error, no data!")
        quit()
    # elif len(data) == 1:
    #     print(f"Automaticly chosen {data[0]}")
    #     return data[0]
    else:
        # List selection options
        for index, data_point in enumerate(data, start=1):
            interactive_print_data(data_point, key, index, ciphers)
            # next_key = common.try_hex_to_string(key) + selection_option['guess']
            # key_to_print = f"key: {next_key}"

            # next_c1xr = selection_option['c1xr-str']
            # c1xr_to_print = f"c1xr: {next_c1xr}"

            # c2xr = selection_option['c2xr-str']
            # c2xr_to_print = f"c2xr: {c2xr}"

            # print(f"\n{i}.\t{key_to_print}\n\t{c1xr_to_print}\n\t{c2xr_to_print}")

        # Interactive selection
        while True:
            try:
                return data[int(input(f"Select: ")) - 1]
            except:
                # Selection failed
                print(f"User input error! Select between 1 and including {len(data)} (Ctrl + C to quit)")
                time.sleep(0.5)
    
    return selected



if __name__ == "__main__":
    # Load data
    print(f"Loading {common.CRIBRESULTFILE}, please wait...")
    with open(common.CRIBRESULTFILE, 'r') as file:
        data = json.load(file)
    
    # Get all ciphers in data set
    ciphers = list(set([item["cipher-1"] for item in data] + [item["cipher-2"] for item in data]))
    print(f"There are {len(ciphers)} ciphers")

    # Calculate target key length
    target_key_len = max([len(item) for item in ciphers])
    print(f"The target key length is {target_key_len}")

    # Iterate over all (likely) combinations and build a key
    key: str = ""
    while len(key) < target_key_len:
        data_at_current_pos = [item for item in data if item['position'] == len(key)]
        key += interactive_selection(data_at_current_pos, key, ciphers)['word']
    print("Done! :)")

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

    quit()