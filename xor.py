def xor_strings(hex1, hex2):
    # XOR two HEX strings
    return ''.join([f"{(int(a, 16) ^ int(b, 16)):x}" for a, b in zip(hex1, hex2)])
