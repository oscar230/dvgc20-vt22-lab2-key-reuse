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
        cx = common.xor_strings(c1, c2)
        print(f"c1={c1} ^ c2={c2} -> cx={cx}")
        for word in common_words:
            for position, drag_result in crib_drag(cx, common.string_to_hex(word)):
                c1xr = common.xor_strings(drag_result, c1)
                c1xr_str = common.try_hex_to_string(c1xr)
                if c1xr_str and is_human_readable(c1xr_str):
                    c2xr = common.xor_strings(drag_result, c2)
                    c2xr_str = common.try_hex_to_string(c2xr)
                    if c2xr_str and is_human_readable(c2xr_str):
                        result = {
                            "cipher1": c1,
                            "cipher2": c2,
                            "cipher-x": cx,
                            "position": position,
                            "guess": word,
                            "drag-result": drag_result,
                            "c1xr-hex": c1xr,
                            "c1xr-str": c1xr_str,
                            "c2xr-hex": c2xr,
                            "c2xr-str": c2xr_str
                        }
                        results.append(result)
    
    #
    #   Write results to disk
    #
    with open(common.CRIBRESULTFILE, "w") as file:
        json.dump(results, file, indent=common.JSONINDENT)
        print(f"Wrote results to file {common.CRIBRESULTFILE}")
