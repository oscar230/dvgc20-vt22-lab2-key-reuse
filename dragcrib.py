import itertools
import json
import common

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
                result = {
                    "c1": c1,
                    "c2": c2,
                    "cx": cx,
                    "word": word,
                    "position": position,
                    "result": drag_result
                }
                results.append(result)

    #
    #   Write results to disk
    #
    with open(common.CRIBRESULTFILE, "w") as file:
        json.dump(results, file, indent=common.JSONINDENT)
        print(f"Wrote results to file {common.CRIBRESULTFILE}")
