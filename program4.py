import itertools
import json

def xor_strings(s1, s2):
    """XOR two strings together and return the result."""
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

def crib_drag(combined_plaintexts, crib):
    """Attempt to drag the crib across the combined plaintexts (result of XORing two ciphertexts)."""
    results = []
    for i in range(len(combined_plaintexts) - len(crib) + 1):
        segment = combined_plaintexts[i:i+len(crib)] # Extract a portion of the combined plaintexts of the same length as the crib
        result = xor_strings(segment, crib)
        results.append((i, result))
    return results

def is_eng(text):
    return len(text) == sum(1 for char in text if char.isalpha() or char.isspace())

if __name__ == "__main__":
    with open("attachment", 'r', encoding="ASCII") as file:
        ciphertexts: list[str] = [item.replace("\n", "") for item in file.readlines()]
    c1 = ciphertexts[0]
    c2 = ciphertexts[1]

    with open("1000eng.txt", 'r', encoding="ASCII") as file:
        common_words: list[str] = [item.replace("\n", "") for item in file.readlines()]

    results = {}
    
    # Iterate over all possible pairs of ciphertexts
    for c1, c2 in itertools.combinations(ciphertexts, 2):
        # Verification to ensure all ciphertexts are used
        used_ciphertexts = set()

        for key in results.keys():
            c1, _, c2 = key.partition("___XOR___")
            used_ciphertexts.add(c1)
            used_ciphertexts.add(c2)

        missing_ciphertexts = set(ciphertexts) - used_ciphertexts

        if not missing_ciphertexts:
            print("All ciphertexts have been used!")
        else:
            print(f"{len(missing_ciphertexts)} ciphertexts were not used")

        # Dump results to a JSON object
        with open("crib_drag_results.json", "w") as outfile:
            json.dump(results, outfile, indent=4)