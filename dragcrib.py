import itertools
import json
import common
import string

def is_human_readable(text) -> bool:
    human_readable_chars = string.ascii_uppercase + string.ascii_lowercase + string.ascii_letters + " ,.!?-_"
    return all(char in human_readable_chars for char in text)

def crib_drag(ciphertexts_xored: str, crib: str) -> list[str]:
    # Attempt to drag the crib across the combined ciphertexts
    results = []
    for i in range(len(ciphertexts_xored) - len(crib) + 1):
        segment = ciphertexts_xored[i:i+len(crib)]
        result = common.xor_strings(segment, crib)
        results.append((i, result))
    return results

if __name__ == "__main__":
    #
    #   Load dependencies
    #
    with open(common.CIPHERFILE, 'r', encoding=common.ENCODING) as file:
        ciphertexts: list[str] = [item.replace("\n", "") for item in file.readlines()]
    with open(common.WORDFILE, 'r', encoding=common.ENCODING) as file:
        common_words: list[str] = [item.replace("\n", "") for item in file.readlines()]

    #
    #   Perform crib drag
    #
    results = []
    for c1, c2 in itertools.combinations(ciphertexts, 2):
        # For each combination of all ciphertexts
        cx = common.xor_strings(c1, c2) # XOR ciphertext 1 and 2
        print(f"c1={c1} ^ c2={c2} -> cx={cx}")
        for word_hex in [common.string_to_hex(item) for item in common_words]:
            # For each word (hex) in the word list
            for position, drag_result in crib_drag(cx, word_hex):
                # For each position in the combined cipertexts

                # Combine cipher 1 and 2 with the crib drag result
                drag_x_1_hex = common.xor_strings(drag_result, c1[position:])
                drag_x_2_hex = common.xor_strings(drag_result, c2[position:])

                # Try and convert results from previous step to strings
                drag_x_1_str = common.try_hex_to_string(drag_x_1_hex)
                drag_x_2_str = common.try_hex_to_string(drag_x_2_hex)

                # If these string are human readable (and not have failed to convert), write result
                if drag_x_1_str and drag_x_2_str and is_human_readable(drag_x_1_str) and is_human_readable(drag_x_2_str):
                    results.append({
                        "cipher-1": c1,
                        "cipher-2": c2,
                        "cipher-x": cx,
                        "position": position,
                        "word": word_hex,
                        "drag-x": drag_result,
                        "drag-x-1": drag_x_1_hex,
                        "drag-x-2": drag_x_2_hex,
                    })
    
    #
    #   Write results to disk
    #
    with open(common.CRIBRESULTFILE, "w") as file:
        json.dump(results, file, indent=common.JSONINDENT)
        print(f"Wrote results to file {common.CRIBRESULTFILE}")

    quit()