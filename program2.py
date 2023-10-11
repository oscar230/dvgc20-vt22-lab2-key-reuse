def xor_strings(s1, s2):
    """XOR two byte sequences together and return the result."""
    return bytes(a ^ b for a, b in zip(s1, s2))


def crib_drag(ciphertext1, ciphertext2, crib):
    """Perform a crib drag on two ciphertexts using the given crib."""
    # Convert hex ciphertexts to bytes
    ct1_bytes = bytes.fromhex(ciphertext1)
    ct2_bytes = bytes.fromhex(ciphertext2)
    
    # Use the shortest ciphertext for XORing
    min_len = min(len(ct1_bytes), len(ct2_bytes))
    
    # XOR the two ciphertexts together up to the length of the shortest ciphertext
    xor_cts = xor_strings(ct1_bytes[:min_len], ct2_bytes[:min_len])
    
    # Convert the crib to bytes for XORing
    crib_bytes = crib.encode('utf-8')
    
    # Try the crib at each position
    for i in range(len(xor_cts) - len(crib_bytes) + 1):
        result = xor_strings(xor_cts[i:i+len(crib_bytes)], crib_bytes)
        # Convert the result back to a string and filter out results with non-printable characters
        result_str = result.decode('utf-8', errors='ignore')
        if all(32 <= ord(c) <= 126 for c in result_str):
            yield i, result_str

# Test crib dragging on the provided ciphertexts with the word "the"
ct1 = "315c4eeaa8b5f8aaf9174145bf43e1784b8fa00dc71d885a804e5ee9fa40b16349c146fb778cdf2d3aff021dfff5b403b510d0d0455468aeb98622b137dae857553ccd8883a7bc37520e06e515d22c954eba5025b8cc57ee59418ce7dc6bc41556bdb36bbca3e8774301fbcaa3b83b220809560987815f65286764703de0f3d524400a19b159610b11ef3e"
ct2 = "234c02ecbbfbafa3ed18510abd11fa724fcda2018a1a8342cf064bbde548b12b07df44ba7191d9606ef4081ffde5ad46a5069d9f7f543bedb9c861bf29c7e205132eda9382b0bc2c5c4b45f919cf3a9f1cb74151f6d551f4480c82b2cb24cc5b028aa76eb7b4ab24171ab3cdadb8356f"

# Collect results
results = list(crib_drag(ct1, ct2, "the"))

results
