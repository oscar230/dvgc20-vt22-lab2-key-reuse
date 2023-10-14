import json

def display_results(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    for key_data, results in data.items():
        print("\nCiphertext pair:", key_data)
        print("\nResults:")

        for idx, result in enumerate(results):
            print(f"{idx + 1}. Crib: {result['crib']}, Position: {result['position']}, Result: {result['result']}")

def build_key_manually(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    selected_key_data = list(data.keys())[0]  # Selecting first pair as default for this example.
    results = data[selected_key_data]

    key_length = max(result['position'] for result in results) + len(results[-1]['result'])
    key = ['?'] * key_length

    while True:
        display_results(json_path)
        selection = input("\nEnter the number of the result you want to include in the key or 'q' to quit: ")

        if selection.lower() == 'q':
            break

        try:
            selected_result = results[int(selection) - 1]
            position = selected_result['position']
            for idx, char in enumerate(selected_result['result']):
                key[position + idx] = char
        except (ValueError, IndexError):
            print("Invalid selection. Please enter a number from the list or 'q' to quit.")

    return ''.join(key)

if __name__ == "__main__":
    json_path = "crib_drag_results.json"
    decryption_key = build_key_manually(json_path)
    print("\nGenerated Decryption Key:", decryption_key)
