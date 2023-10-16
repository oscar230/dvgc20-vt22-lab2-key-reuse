import itertools
import json
import common
import string

def is_human_readable(text) -> bool:
    human_readable_chars = string.ascii_uppercase + string.ascii_lowercase + string.ascii_letters + ' ' + '.' #string.printable[:-5]
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
        common_words: list[str] = [item.replace("\n", "") for item in file.readlines()][:5]

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
                drag_x_1_str = common.xor_strings(drag_result, c1)
                c1xr_str = common.try_hex_to_string(drag_x_1_str)
                c2xr = common.xor_strings(drag_result, c2)
                drag_x_2_str = common.try_hex_to_string(c2xr)
                if c1xr_str and drag_x_2_str and is_human_readable(c1xr_str) and is_human_readable(drag_x_2_str):
                    results.append({
                        "position": position,
                        "cipher-1-hex": c1,
                        "cipher-2-hex": c2,
                        "cipher-x-hex": cx,
                        "word-hex": word_hex,
                        "drag-x-hex": drag_result,
                        "drag-x-1-hex": drag_x_1_str,
                        "drag-x-2-hex": c1xr_str,
                        "drag-x-1-str": drag_x_1_str,
                        "drag-x-2-str": drag_x_2_str,
                    })
    
    #
    #   Write results to disk
    #
    with open(common.CRIBRESULTFILE, "w") as file:
        json.dump(results, file, indent=common.JSONINDENT)
        print(f"Wrote results to file {common.CRIBRESULTFILE}")
