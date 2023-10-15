import itertools
import json
import common

def xor_strings(s1, s2):
    """XOR two strings together and return the result."""
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

def crib_drag(combined_plaintexts, crib):
    """Attempt to drag the crib across the combined plaintexts (result of XORing two ciphertexts)."""
    results = []
    for i in range(len(combined_plaintexts) - len(crib) + 1):
        segment = combined_plaintexts[i:i+len(crib)]
        result = xor_strings(segment, crib)
        results.append((i, result))
    return results

def is_eng(text):
    return len(text) == sum(1 for char in text if char.isalpha() or char.isspace())

if __name__ == "__main__":

    #
    #   Load dependencies
    #
    with open(common.CIPHERFILE, 'r', encoding="ASCII") as file:
        ciphertexts: list[str] = [item.replace("\n", "") for item in file.readlines()][:3]
    with open(common.WORDFILE, 'r', encoding="ASCII") as file:
        common_words: list[str] = [item.replace("\n", "") for item in file.readlines()][:50]

    #
    #   Perform crib drag
    #
    results = {}
    for c1, c2 in itertools.combinations(ciphertexts, 2):
        xor_combined_plaintexts = xor_strings(c1, c2)
        for crib in common_words:
            for position, result in crib_drag(xor_combined_plaintexts, crib):
                if is_eng(result):
                    key = f"{c1}___XOR___{c2}"
                    if key not in results:
                        results[key] = []
                    results[key].append({"crib": crib, "position": position, "result": result})

    #
    #   Verify results
    #
    used_ciphertexts = set()
    for key in results.keys():
        c1, _, c2 = key.partition("___XOR___")
        used_ciphertexts.add(c1)
        used_ciphertexts.add(c2)
    if used_ciphertexts == set(ciphertexts):
        print("All ciphertexts have been used!")
    else:
        missing_ciphertexts = set(ciphertexts) - used_ciphertexts
        print(f"{len(missing_ciphertexts)} ciphertexts were not used!")

    #
    #   Write results to disk
    #
    with open(common.CRIBRESULTFILE, "w") as file:
        json.dump(results, file, indent=common.JSONINDENT)
        print(f"Wrote results to file {common.CRIBRESULTFILE}")