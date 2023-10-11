def xor_hex_strings(hex_str1, hex_str2):
    """XOR two hex strings."""
    xor_result = int(hex_str1, 16) ^ int(hex_str2, 16)
    return '{:x}'.format(xor_result).zfill(len(hex_str1))


def crib_drag(ciphertext1, ciphertext2, crib):
    """Perform the crib dragging attack."""
    # Convert crib to hex
    crib_hex = crib.encode().hex()
    
    # XOR the two ciphertexts
    xor_result = xor_hex_strings(ciphertext1, ciphertext2)
    
    # This will store the results
    results = []
    
    for i in range(len(xor_result) - len(crib_hex) + 1):
        # XOR part of the XORed ciphertexts with the crib
        xor_with_crib = xor_hex_strings(xor_result[i:i+len(crib_hex)], crib_hex)
        
        # Convert the result back to ASCII
        try:
            text = bytes.fromhex(xor_with_crib).decode()
            results.append((i, text))
        except:
            # There might be decoding errors if it's not valid ASCII
            pass
        
    return results


# Let's test the crib_drag function with the provided ciphertexts and the word "the"
ciphertexts = [
    "315c4eeaa8b5f8aaf9174145bf43e1784b8fa00dc71d885a804e5ee9fa40b16349c146fb778cdf2d3aff021dfff5b403b510d0d0455468aeb98622b137dae857553ccd8883a7bc37520e06e515d22c954eba5025b8cc57ee59418ce7dc6bc41556bdb36bbca3e8774301fbcaa3b83b220809560987815f65286764703de0f3d524400a19b159610b11ef3e",
    "234c02ecbbfbafa3ed18510abd11fa724fcda2018a1a8342cf064bbde548b12b07df44ba7191d9606ef4081ffde5ad46a5069d9f7f543bedb9c861bf29c7e205132eda9382b0bc2c5c4b45f919cf3a9f1cb74151f6d551f4480c82b2cb24cc5b028aa76eb7b4ab24171ab3cdadb8356f",
    "32510ba9a7b2bba9b8005d43a304b5714cc0bb0c8a34884dd91304b8ad40b62b07df44ba6e9d8a2368e51d04e0e7b207b70b9b8261112bacb6c866a232dfe257527dc29398f5f3251a0d47e503c66e935de81230b59b7afb5f41afa8d661cb"
]

# List of common English words to use as cribs
cribs = [
    ".", " ", "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
    "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
    "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
    "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
    "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
    "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
    "even", "new", "want", "because", "any", "these", "give", "day", "most", "us"
]

# Dictionary to store results for each crib
crib_results = {}

# Dragging each crib across the XOR of the first two ciphertexts
for crib in cribs:
    crib_results[crib] = crib_drag(ciphertexts[0], ciphertexts[1], crib)

print(crib_results)
