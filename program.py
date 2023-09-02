ENCODING: str = "utf-8"
INPUT_FILE_NAME: str = "attachment2"
COMMON_ENG: list[str] = [
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

def xor_strings(string_a: str, string_b: str) -> str:
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(string_a, string_b))

def crib_drag(cipher_a: str, cipher_2: str, crib_text: str) -> None:
    ciphers_xored = xor_strings(cipher_a, cipher_2)
    crib_text_length = len(crib_text)

    for i in range(len(ciphers_xored) - crib_text_length + 1):
        crib_result = xor_strings(ciphers_xored[i:i + crib_text_length], crib_text)
        if crib_result == crib_text:
            print(f"Pos:{i} for {crib_result}")

    return None

def pwn(ciphertexts: list[str]) -> None:
    ciphertexts_as_hex_strings: list[str] = [item.encode(encoding=ENCODING).hex() for item in ciphertexts]
    print(f"{len(ciphertexts_as_hex_strings)} ciphertexts")
    for a in ciphertexts:
        for b in ciphertexts:
            if a != b:
                for word in COMMON_ENG:
                    print(f"a={a}\nb={b}")
                    crib_drag(a, b, word)
                    return None

if __name__ == "__main__":
    with open(INPUT_FILE_NAME, 'r', encoding=ENCODING) as file:
        input: list[str] = [item.replace("\n", "") for item in file.readlines()]
    pwn(input)