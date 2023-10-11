import itertools

def xor_strings(s1, s2):
    """XOR two strings together and return the result."""
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

def crib_drag(combined_plaintexts, crib):
    """Attempt to drag the crib across the combined plaintexts (result of XORing two ciphertexts)."""
    results = []
    for i in range(len(combined_plaintexts) - len(crib) + 1):
        # Extract a portion of the combined plaintexts of the same length as the crib
        segment = combined_plaintexts[i:i+len(crib)]
        
        # XOR the segment with the crib
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

    xor_combined_plaintexts = xor_strings(c1, c2)

    with open("1000eng.txt", 'r', encoding="ASCII") as file:
        cribs: list[str] = [item.replace("\n", "") for item in file.readlines()]

    for crib in cribs[:100]:
        print("Starting crib dragging...\n")
        for position, result in crib_drag(xor_combined_plaintexts, crib):
            if is_eng(result):
                print(f"{crib}\t{position}\t{result}")
